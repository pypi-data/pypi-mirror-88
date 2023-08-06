import abc
import json
import uuid
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass, field, replace
from logging import Logger
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
)

import grpc
from pandas import DataFrame as PDataFrame
from pyspark.sql import DataFrame as SDataFrame, SparkSession

from .api.entity.dataset_build_pb2 import DatasetBuild as PBDatasetBuild
from .api.entity.dataset_list_options_pb2 import DatasetListOptions, DatasetSortField
from .api.entity.dataset_pb2 import Dataset as PBDataset
from .api.entity.dataset_version_pb2 import DatasetVersion as PBDatasetVersion
from .api.entity.feature_set_list_options_pb2 import FeatureSetListOptions
from .api.entity.feature_set_pb2 import FeatureSet as PBFeatureSet
from .api.entity.model_train_pb2 import ModelTrain
from .api.entity.model_version_pb2 import ModelVersion
from .api.entity.sql_feature_pb2 import SqlFeature as PBSqlFeature
from .api.ids_pb2 import (
    AppId,
    DatasetBuildId,
    DatasetId,
    DatasetVersionId,
    FeatureSetId,
    ModelTrainId,
    OrganizationId,
    UserId,
)
from .api.service.datacatalog.data_catalog_api_pb2 import (
    AddFeatureSetRequest,
    CompleteBuildRequest,
    GetBuildRequest,
    GetDatasetRequest,
    GetDatasetsRequest,
    GetFeatureSetByNameRequest,
    GetFeatureSetRequest,
    GetLatestBuildRequest,
    GetVersionRequest,
    InitiateBuildRequest,
)
from .api.service.datacatalog.data_catalog_api_pb2_grpc import DataCatalogAPIStub
from .api.service.featureengine.feature_engine_api_pb2 import BuildFeaturesRequest
from .api.service.featureengine.feature_engine_api_pb2_grpc import FeatureEngineAPIStub
from .api.service.modelcatalog.model_catalog_api_pb2 import (
    CompleteModelTrainRequest,
    GetModelTrainRequest,
    GetModelVersionRequest,
    LoadModelTrainDataRequest,
    LogMetricValueRequest,
    LogMetricValueResponse,
    LogModelTrainParametersRequest,
    LogModelTrainParametersResponse,
    StartModelTrainRequest,
)
from .api.service.modelcatalog.model_catalog_api_pb2_grpc import ModelCatalogAPIStub
from .api.value.aws_credentials_pb2 import AwsCredentials
from .api.value.metadata_pb2 import Metadata
from .api.value.s3_path_pb2 import S3Path
from .api.value.signature_pb2 import Signature
from .api.value.storage_location_pb2 import StorageLocation
from .config import LayerClientConfig
from .exceptions import LayerClientException
from .mlmodels import MlModelInferableDataset, ModelObject
from .mlmodels.flavors import ModelFlavor
from .mlmodels.flavors.model_definition import ModelDefinition
from .mlmodels.service import MLModelService


_MAX_FAILURE_INFO_LENGTH = 200


@dataclass(frozen=True)
class Dataset:
    name: str

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    version: str = ""
    schema: str = "{}"
    uri: str = ""
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Feature(abc.ABC):
    name: str
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class SQLFeature(Feature):
    query: str = ""


@dataclass(frozen=True)
class Featureset:
    name: str
    features: List[Feature]
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True)
class SortField:
    name: str
    descending: bool = False


@dataclass(frozen=True)
class StartTrainMetadata:
    train_id: ModelTrainId  # type: ignore
    s3_path: S3Path  # type: ignore
    credentials: AwsCredentials  # type: ignore


class SortBy:
    NAME_ASC = SortField("name")
    NAME_DESC = SortField("name", True)


class DataCatalogClient:
    _service: DataCatalogAPIStub
    _feature_engine_service: FeatureEngineAPIStub

    def __init__(
        self,
        config: LayerClientConfig,
        logger: Logger,
        session: SparkSession,
        *,
        service_factory: Callable[..., DataCatalogAPIStub] = DataCatalogAPIStub,
        feature_engine_service_factory: Callable[
            ..., FeatureEngineAPIStub
        ] = FeatureEngineAPIStub,
    ):
        self._user_id = config.user_id
        self._client_id = config.client_id
        self._config = config.data_catalog
        self._session = session
        self._logger = logger
        self._service_factory = service_factory
        self._feature_engine_service_factory = feature_engine_service_factory
        self._call_metadata = [("authorization", f"Bearer {config.access_token}")]

    @contextmanager
    def init(self) -> Iterator["DataCatalogClient"]:
        with grpc.insecure_channel(self._config.address) as channel:
            self._service = self._service_factory(channel)
            self._feature_engine_service = self._feature_engine_service_factory(channel)
            yield self

    def add_featureset(self, featureset: Featureset) -> Featureset:
        sql_features = []
        for feature in featureset.features:
            if not isinstance(feature, SQLFeature):
                raise TypeError(f"Unsupported type: {feature.__class__!r}")
            sql_features.append(
                PBSqlFeature(
                    name=feature.name,
                    query_text=feature.query,
                )
            )
        resp = self._service.AddFeatureSet(
            AddFeatureSetRequest(
                feature_set=PBFeatureSet(
                    name=featureset.name,
                    sql_features=sql_features,
                )
            ),
            metadata=self._call_metadata,
        )
        return self.get_featureset_by_id(uuid.UUID(resp.feature_set_id.value))

    def get_featureset_by_id(self, id_: uuid.UUID) -> Featureset:
        resp = self._service.GetFeatureSet(
            GetFeatureSetRequest(feature_set_id=FeatureSetId(value=str(id_))),
            metadata=self._call_metadata,
        )
        return self._create_featureset(resp.feature_set)

    def get_featureset_by_name(self, name: str) -> Featureset:
        resp = self._service.GetFeatureSetByName(
            GetFeatureSetByNameRequest(feature_set_name=name),
            metadata=self._call_metadata,
        )
        return self._create_featureset(resp.feature_set)

    def list_featuresets(self) -> Iterator[Featureset]:
        resp = self._service.GetFeatureSets(
            GetFeatureSetRequest(
                dataset_list_options=FeatureSetListOptions(page_size=1000)
            ),
            metadata=self._call_metadata,
        )

        for feature_set in resp.feature_sets:
            yield self._create_featureset(feature_set)

    def _create_featureset(self, feature_set: PBFeatureSet) -> Featureset:  # type: ignore
        features: List[Feature] = []
        for feature in feature_set.sql_features:  # type: ignore
            features.append(
                SQLFeature(
                    id=uuid.UUID(feature.id.value),
                    name=feature.name,
                    query=feature.query_text,
                )
            )
        return Featureset(
            id=uuid.UUID(feature_set.id.value),  # type: ignore
            name=feature_set.name,  # type: ignore
            features=features,
        )

    def build_features(self, names: List[str]) -> Dataset:
        resp = self._feature_engine_service.BuildFeatures(
            BuildFeaturesRequest(features=names),
            metadata=self._call_metadata,
        )
        build = resp.build
        if build.build_info.status != PBDatasetBuild.BuildStatus.BUILD_STATUS_COMPLETED:  # type: ignore
            raise LayerClientException(
                f"Build {build.id.value!r} failed: {build.build_info.info}"
            )
        return self._create_dataset(resp.dataset, resp.version, build)

    def add_dataset(self, dataset: Dataset) -> Dataset:
        self._logger.debug(
            "Adding a new dataset with name %r and version %r",
            dataset.name,
            dataset.version,
        )
        init_resp = self._service.InitiateBuild(
            InitiateBuildRequest(
                dataset_name=dataset.name,
                dataset_version=dataset.version or "",
                build_description="",
                format="unused",
                user=UserId(value=str(self._user_id)),
                schema=dataset.schema,
            ),
            metadata=self._call_metadata,
        )
        comp_resp = self._service.CompleteBuild(
            CompleteBuildRequest(
                id=init_resp.id,
                status=PBDatasetBuild.BuildStatus.BUILD_STATUS_COMPLETED,  # type: ignore
                success=CompleteBuildRequest.BuildSuccess(  # type: ignore
                    location=StorageLocation(
                        uri=dataset.uri, metadata=Metadata(value=dataset.metadata)
                    )
                ),
            ),
            metadata=self._call_metadata,
        )
        return replace(
            dataset,
            id=uuid.UUID(comp_resp.version.dataset_id.value),
            version=comp_resp.version.name,
        )

    def get_dataset_by_id(self, id_: uuid.UUID) -> Dataset:
        dataset = self._get_dataset_by_id(str(id_))
        build = self._get_build_by_id(dataset.default_build_id.value)  # type: ignore
        version = self._get_version_by_id(build.dataset_version_id.value)  # type: ignore
        return self._create_dataset(dataset, version, build)

    def get_dataset_by_name(self, name: str, version: Optional[str] = None) -> Dataset:
        build = self._get_build_by_name(name, version)
        version = self._get_version_by_id(build.dataset_version_id.value)  # type: ignore
        dataset = self._get_dataset_by_id(version.dataset_id.value)
        return self._create_dataset(dataset, version, build)

    def list_datasets(
        self,
        sort_fields: Sequence[SortField] = (),
        query_build: bool = True,
    ) -> Iterator[Dataset]:
        for dataset in self._list_datasets(sort_fields):
            if query_build:
                build = self._get_build_by_id(dataset.default_build_id.value)  # type: ignore
                version = self._get_version_by_id(build.dataset_version_id.value)  # type: ignore
            else:
                build = PBDatasetBuild()
                version = PBDatasetVersion()
            yield self._create_dataset(dataset, version, build)

    def _create_dataset(
        self,
        dataset: PBDataset,  # type: ignore
        version: PBDatasetVersion,  # type: ignore
        build: PBDatasetBuild,  # type: ignore
    ) -> Dataset:
        return Dataset(
            id=uuid.UUID(dataset.id.value),  # type: ignore
            name=dataset.name,  # type: ignore
            version=version.name,  # type: ignore
            schema=version.schema,  # type: ignore
            uri=build.location.uri,  # type: ignore
            metadata=dict(build.location.metadata.value),  # type: ignore
        )

    def _get_dataset_by_id(self, id_: str) -> PBDataset:  # type: ignore
        return self._service.GetDataset(
            GetDatasetRequest(dataset_id=DatasetId(value=id_)),
            metadata=self._call_metadata,
        ).dataset

    def _get_version_by_id(self, id_: str) -> PBDatasetVersion:  # type: ignore
        return self._service.GetVersion(
            GetVersionRequest(version_id=DatasetVersionId(value=id_)),
            metadata=self._call_metadata,
        ).version

    def _get_build_by_id(self, id_: str) -> PBDatasetBuild:  # type: ignore
        return self._service.GetBuild(
            GetBuildRequest(build_id=DatasetBuildId(value=id_)),
            metadata=self._call_metadata,
        ).build

    def _get_build_by_name(
        self, name: str, version: Optional[str] = None
    ) -> PBDatasetBuild:  # type: ignore
        return self._service.GetLatestBuild(
            GetLatestBuildRequest(
                dataset_name=name,
                dataset_version=version,
            ),
            metadata=self._call_metadata,
        ).build

    def _list_datasets(
        self, sort_fields: Sequence[SortField] = ()
    ) -> List[PBDataset]:  # type: ignore
        return self._service.GetDatasets(
            GetDatasetsRequest(
                dataset_list_options=DatasetListOptions(
                    sorting=[
                        DatasetSortField(
                            name=sort_field.name, descending=sort_field.descending
                        )
                        for sort_field in sort_fields
                    ]
                )
            ),
            metadata=self._call_metadata,
        ).datasets

    def load(self, name: str, version: Optional[str] = None) -> SDataFrame:
        self._logger.debug(
            "Loading data object with name %r and version %r", name, version
        )
        build = self._get_build_by_name(name, version)
        return self._session.read.parquet(build.location.uri)  # type: ignore

    def save(
        self,
        name: str,
        obj: Union[PDataFrame, SDataFrame],
        version: Optional[str] = None,
    ) -> PBDatasetBuild:  # type: ignore
        self._logger.debug(
            "Saving data object with name %r and version %r", name, version
        )
        df: SDataFrame
        if isinstance(obj, PDataFrame):
            df = self._session.createDataFrame(obj)
        else:
            df = obj

        schema = json.dumps(df.schema.jsonValue())
        init_resp = self._service.InitiateBuild(
            InitiateBuildRequest(
                dataset_name=name,
                dataset_version=version or "",
                build_description="",
                format="parquet",
                user=UserId(value=str(self._user_id)),
                schema=schema,
            ),
            metadata=self._call_metadata,
        )

        uri = f"s3a://{self._config.s3_bucket_name}/{init_resp.suggested_path}"
        exception: Optional[Exception] = None
        try:
            df.write.mode("overwrite").parquet(uri)
        except Exception as exc:
            exception = exc
            comp_req = CompleteBuildRequest(
                id=init_resp.id,
                status=PBDatasetBuild.BuildStatus.BUILD_STATUS_FAILED,  # type: ignore
                failure=CompleteBuildRequest.BuildFailed(  # type: ignore
                    info=str(exc)[:_MAX_FAILURE_INFO_LENGTH]
                ),
            )
        else:
            comp_req = CompleteBuildRequest(
                id=init_resp.id,
                status=PBDatasetBuild.BuildStatus.BUILD_STATUS_COMPLETED,  # type: ignore
                success=CompleteBuildRequest.BuildSuccess(  # type: ignore
                    location=StorageLocation(uri=uri)
                ),
            )

        comp_resp = self._service.CompleteBuild(
            comp_req,
            metadata=self._call_metadata,
        )

        if exception:
            raise exception

        return comp_resp.build


class ModelCatalogClient:
    _service: ModelCatalogAPIStub

    def __init__(
        self,
        config: LayerClientConfig,
        ml_model_service: MLModelService,
        logger: Logger,
    ):
        self._client_id = config.client_id
        self._user_id = config.user_id
        self._config = config.model_catalog
        self._org_id: uuid.UUID = config.organization_id
        self._logger = logger
        self._ml_model_service = ml_model_service
        self._call_metadata = [("authorization", f"Bearer {config.access_token}")]

    @contextmanager
    def init(self) -> Iterator["ModelCatalogClient"]:
        with grpc.insecure_channel(self._config.address) as channel:
            self._service = ModelCatalogAPIStub(channel=channel)  # type: ignore
            yield self

    def load(
        self,
        name: str,
        version_name: Optional[int] = None,
        train_number: Optional[int] = None,
    ) -> Any:
        """
        Loads a model from the model catalog

        :param name: the name of the model
        :param version_name: the version of the model
        :param train_number: the train number of the model
        :return: a model definition
        """
        self._logger.debug(f"Loading model object with name {name}")
        load_response = self._service.LoadModelTrainData(
            LoadModelTrainDataRequest(
                organization_id=OrganizationId(value=str(self._org_id)),
                model_name=name,
                model_version=None if version_name is None else str(version_name),
                model_train=train_number,
            ),
            metadata=self._call_metadata,
        )
        train: ModelTrain = self._service.GetModelTrain(  # type: ignore
            GetModelTrainRequest(
                model_train_id=load_response.id,
            ),
            metadata=self._call_metadata,
        ).model_train
        version: ModelVersion = self._service.GetModelVersion(  # type: ignore
            GetModelVersionRequest(
                model_version_id=train.model_version_id,  # type: ignore
            ),
            metadata=self._call_metadata,
        ).version

        model_definition = ModelDefinition(
            name=name,
            version=version.name,  # type: ignore
            train_number=train.index,  # type: ignore
            signature=version.signature,  # type: ignore
            proto_flavor=load_response.flavor,
            s3_path=load_response.s3_path,
            credentials=load_response.credentials,
        )
        self._logger.debug(f"Model definition: {model_definition}")
        return self._ml_model_service.retrieve(model_definition)

    def infer_signature(
        self,
        model_input: MlModelInferableDataset,
        model_output: MlModelInferableDataset,
    ) -> Signature:  # type: ignore
        return self._ml_model_service.get_model_signature(model_input, model_output)

    def save_model(
        self,
        model_definition: ModelDefinition,
        trained_model_obj: ModelObject,
    ) -> ModelObject:
        flavor = self._ml_model_service.get_model_flavor_from_proto(
            model_definition.proto_flavor
        )
        if not flavor:
            raise LayerClientException("Model flavor not found")
        self._logger.debug(
            f"Storing given model {trained_model_obj} with definition {model_definition}"
        )
        self._ml_model_service.store(
            model_definition=model_definition,
            model_object=trained_model_obj,
            flavor=flavor,
        )
        return trained_model_obj

    def start_model_train(
        self,
        name: str,
        version: Optional[int],
        signature: Signature,  # type: ignore
        proto_flavor: ModelFlavor,
    ) -> StartTrainMetadata:
        organization_id: uuid.UUID = self._org_id
        response = self._service.StartModelTrain(
            StartModelTrainRequest(
                organization_id=OrganizationId(value=str(organization_id)),
                app_id=AppId(value=str(self._client_id)),
                user_id=UserId(value=str(self._user_id)),
                model_name=name,
                model_version=None if version is None else str(version),
                flavor=proto_flavor,
                signature=signature,
            ),
            metadata=self._call_metadata,
        )
        return StartTrainMetadata(
            train_id=response.id,
            s3_path=response.s3_path,
            credentials=response.credentials,
        )

    def infer_flavor(self, model_obj: ModelObject) -> Any:
        tup: Tuple[Any, ModelFlavor] = self._ml_model_service.get_model_flavor(
            model_obj
        )
        return tup[0]

    def complete_model_train(self, train_id: ModelTrainId) -> None:  # type: ignore
        self._service.CompleteModelTrain(
            CompleteModelTrainRequest(id=train_id),
            metadata=self._call_metadata,
        )

    def log_parameter(self, train_id: ModelTrainId, name: str, value: str) -> None:  # type: ignore
        """
        Logs given parameter to the model catalog service

        :param train_id: id of the train to associate params with
        :param name: parameter name
        :param value: parameter value
        """
        self.log_parameters(train_id, {name: value})

    def log_parameters(
        self, train_id: ModelTrainId, parameters: Dict[str, str]  # type: ignore
    ) -> None:
        """
        Logs given parameters to the model catalog service

        :param train_id: id of the train to associate params with
        :param parameters: map of parameter name to its value
        """
        response: LogModelTrainParametersResponse = (  # type: ignore
            self._service.LogModelTrainParameters(
                LogModelTrainParametersRequest(
                    train_id=train_id,
                    parameters=parameters,
                ),
                metadata=self._call_metadata,
            )
        )
        self._logger.debug(f"LogModelTrainParameters response: {str(response)}")

    def log_metric(
        self, train_id: ModelTrainId, name: str, value: float, timestamp: int  # type: ignore
    ) -> None:
        """
        Logs given metric to the model storage service

        :param train_id: corresponding model train id
        :param name: name of the metric
        :param value: value of the metric
        :param timestamp: relative to start of training
        """
        response: LogMetricValueResponse = self._service.LogMetricValue(  # type: ignore
            LogMetricValueRequest(
                model_train_id=train_id,
                name=name,
                value=value,
                timestamp=timestamp,
            ),
            metadata=self._call_metadata,
        )
        self._logger.debug(f"LogMetricValue response: {str(response)}")


class LayerClient:
    def __init__(
        self, config: LayerClientConfig, logger: Logger, session: SparkSession
    ):
        self._config = config
        self._data_catalog = DataCatalogClient(config, logger, session)
        ml_model_service = MLModelService(logger)
        self._model_catalog = ModelCatalogClient(config, ml_model_service, logger)

    @contextmanager
    def init(self) -> Iterator["LayerClient"]:
        with ExitStack() as exit_stack:
            if self._config.data_catalog.is_enabled:
                exit_stack.enter_context(self._data_catalog.init())
            if self._config.model_catalog.is_enabled:
                exit_stack.enter_context(self._model_catalog.init())
            yield self

    @property
    def data_catalog(self) -> DataCatalogClient:
        return self._data_catalog

    @property
    def model_catalog(self) -> ModelCatalogClient:
        return self._model_catalog
