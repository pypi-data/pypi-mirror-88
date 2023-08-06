import re
import unicodedata

from ...api.entity.model_pb2 import Model  # pylint: disable=unused-import
from ...api.value.aws_credentials_pb2 import AwsCredentials
from ...api.value.s3_path_pb2 import S3Path
from ...api.value.signature_pb2 import Signature


class ModelDefinition:
    """Holds information regarding an ML model.

    This class holds structural information about an ML Model and is able to construct a path where
    you can find the model in the storage. It also stores the metadata associated with the corresponding model train.
    """

    def __init__(
        self,
        name: str,
        version: int,
        train_number: int,
        signature: Signature,
        proto_flavor: Model.ModelFlavor,
        s3_path: S3Path,
        credentials: AwsCredentials,
    ):
        self.__model_name: str = slugify(name).replace("-", "")
        self.__version: int = version
        self.__train_number: int = train_number
        self.__signature: Signature = signature
        self.__proto_flavor: Model.ModelFlavor = proto_flavor
        self.__s3_path: S3Path = s3_path
        self.__credentials: AwsCredentials = credentials

    @property
    def model_name(self) -> str:
        """Returns the model name

        Returns:
            A string name, as it is in the stored metadata
        """
        return self.__model_name

    @property
    def model_version(self) -> int:
        """Returns the model version

        Returns:
            An int, as it is in the stored metadata
        """
        return self.__version

    @property
    def model_train_number(self) -> int:
        """Returns the model train's number

        Returns:
            An int, as it is in the stored metadata
        """
        return self.__train_number

    @property
    def model_signature(self) -> Signature:
        """Returns the model signature

        Returns:
            A Signature that specifies the input and output types of a model, as it is in the stored metadata
        """
        return self.__signature

    @property
    def proto_flavor(self) -> Model.ModelFlavor:
        """Returns the proto flavor

        Returns:
            A string - the proto flavor, used to infer the type of the model obj to instantiate
        """
        return self.__proto_flavor

    @property
    def s3_path(self) -> S3Path:
        """Returns the s3 path where the model is stored

        Returns:
            A S3Path proto - The s3 path where the model is stored
        """
        return self.__s3_path

    @property
    def credentials(self) -> AwsCredentials:
        """Returns the credentials object for this model

        Returns:
            A AwsCredentials proto - The credentials object for this model
        """
        return self.__credentials

    def __repr__(self) -> str:
        return (
            f"ModelDefinition{{"
            f"model_name:{self.model_name}"
            f"model_version:{self.model_version}"
            f"model_train_number:{self.model_train_number}"
            f"model_signature:{self.model_signature}"
            f"proto_flavor:{self.proto_flavor}"
            f"s3_path:{self.s3_path}"
            f"}}"
        )


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.

    Taken unchanged from django/utils/text.py
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)
