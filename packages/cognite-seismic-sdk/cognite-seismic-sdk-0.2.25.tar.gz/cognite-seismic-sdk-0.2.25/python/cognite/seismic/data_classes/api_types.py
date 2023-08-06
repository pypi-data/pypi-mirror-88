import json
import os
from typing import List, Mapping, Optional, Tuple, Union

from cognite.seismic._api.utility import MaybeString

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos.types_pb2 import (
        Geometry as GeometryProto,
        IngestionSource,
        CRS as CRSProto,
        GeoJson,
        Wkt,
    )
    from cognite.seismic.protos.v1.seismic_service_datatypes_pb2 import (
        TextHeader as TextHeaderProto,
        BinaryHeader as BinaryHeaderProto,
    )
else:
    from enum import Enum

    class IngestionSource(Enum):
        """Enum of ingestion sources."""

        INVALID_SOURCE = 0
        """Indicates that a source was not specified or was invalid."""
        FILE_SOURCE = 1
        """Indicates ingestion from a file"""
        TRACE_WRITER = 2
        """Indicates creation by trace writer"""


# Contains types returned by the SDK API.


class Coordinate:
    """Represents physical coordinates in a given CRS.
    
    Attributes:
        crs (str): The coordinate reference system of the coordinate. Generally should be an EPSG code.
        x (float): The x value of the coordinate.
        y (float): The y value of the coordinate.
    """

    crs: str
    x: float
    y: float

    def __init__(self, crs, x, y):
        self.crs = crs
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Coordinate<crs: {self.crs}, x: {self.x}, y: {self.y}>"

    @staticmethod
    def from_proto(proto) -> "Coordinate":
        return Coordinate(crs=proto.crs, x=proto.x, y=proto.y)


class Trace:
    """Represents a seismic trace with a single inline / crossline coordinate.
    
    Attributes:
        trace_header (bytes): The raw trace header.
        inline (int): The inline number
        crossline (int): The crossline number
        trace (List[float]): The trace values
        coordinate (:py:class:`Coordinate`): The coordinate of the trace
    """

    trace_header: bytes
    inline: int
    crossline: int
    trace: List[float]
    coordinate: Coordinate

    def __init__(self, trace_header, inline, crossline, trace, coordinate):
        self.trace_header = trace_header
        self.inline = inline
        self.crossline = crossline
        self.trace = trace
        self.coordinate = coordinate

    def __repr__(self):
        return f"Trace<inline: {self.inline}, crossline: {self.crossline}, coordinates: {str(self.coordinate)}, trace: {self.trace}>"

    @staticmethod
    def from_proto(proto) -> "Trace":
        return Trace(
            trace_header=proto.trace_header,
            inline=proto.iline.value,
            crossline=proto.xline.value,
            trace=proto.trace,
            coordinate=Coordinate.from_proto(proto.coordinate),
        )


class VolumeDef:
    """Represents a VolumeDef, a method to describe an inline/crossline grid. Refer to :ref:`VolumeDef Overview` for more information.
    
    """

    json: str

    def __init__(self, json_payload):
        self.json = json_payload
        self.parsed = json.loads(json_payload)

    def __repr__(self):
        return f"VolumeDef<{self.json}>"

    @staticmethod
    def from_proto(proto) -> "VolumeDef":
        return VolumeDef(json_payload=proto.json)

    @staticmethod
    def _get_method_size(method) -> int:
        """Given a volumedef method, calculate the number of traces within it"""
        c = 0
        if "list" in method:
            c += len(method["list"])
        elif "range" in method:
            range_ = method["range"]
            if len(range_) == 3:
                step = range_[2]
            else:
                # Accounting for negative ranges
                if range_[0] < range_[1]:
                    step = 1
                else:
                    step = -1
            c += (range_[1] - range_[0]) // step + 1
        else:
            raise Exception(f"The specified method {method} was not recognized.")

        return c

    def count_line_traces(self) -> Mapping[int, int]:
        """Count the number of traces by line.
        
        Returns:
            Mapping[int, int]: A mapping of line number to trace count.
        """
        if self.parsed["version"] > 101:
            raise Exception(
                f'The specified volumedef version {self.parsed["version"]} is not supported by this version of the Cognite SDK.'
            )
        output = {}
        for key, methods in self.parsed["lines"].items():
            c = 0
            for method in methods:
                c += VolumeDef._get_method_size(method)
            output[int(key)] = c
        return output

    def count_total_traces(self) -> int:
        """Count the total number of traces in this volumedef."""
        c = 0
        traces = self.count_line_traces()
        for val in traces.values():
            c += val
        return c


class File:
    """Represents a raw SEGY file.
    
    Attributes:
        id (str): The id of the file
        name (str): The name of the file
        metadata (Mapping[str, str]): Any custom-defined metadata for the file
        is_temporary (bool): `True` if the file is temporary.
    """

    id: str
    name: str
    metadata: Mapping[str, str]
    is_temporary: bool

    def __init__(self, *, id, name, metadata, is_temporary):
        self.id = id
        self.name = name
        self.metadata = metadata
        self.is_temporary = is_temporary

    def __repr__(self):
        temporary = ", temporary" if self.is_temporary else ""
        return f"File<id: {self.id}, name: {self.name}{temporary}, metadata: {metadata}>"

    @staticmethod
    def from_proto(proto) -> "File":
        metadata = {}
        for key in proto.metadata:
            metadata[key] = proto.metadata[key]
        return File(id=proto.id, name=proto.name, metadata=metadata, is_temporary=proto.is_temporary)


class Geometry:
    """Represents a CRS + shape, in either a WKT format or a GeoJSON.
    
    Attributes:
        crs (str): The CRS of the shape.
        geojson (Optional[dict]): If exists, the GeoJSON representation of this shape
        wkt (Optional[str]): If exists, the Well Known Text representation of this shape
    """

    crs: str
    geojson: Optional[dict]
    wkt: Optional[str]

    def __init__(self, crs: str, *, geojson=None, wkt=None):
        if (geojson is None) and (wkt is None):
            raise ValueError("You must specify one of: geojson, wkt")
        if (geojson is not None) and (wkt is not None):
            raise ValueError("You must specify either of: geojson, wkt")
        self.crs = crs
        self.geojson = geojson
        self.wkt = wkt

    def __repr__(self):
        if geojson:
            return f"Geometry<crs: {self.crs}, geojson: {self.geojson}>"
        else:
            return f"Geometry<crs: {self.crs}, wkt: {self.wkt}>"

    @staticmethod
    def from_proto(proto) -> Union["Geometry", None]:
        """Convert a Geometry proto into a Geometry object.

        May return None if neither geojson nor wkt are specified.        
        """
        crs = proto.crs.crs
        # TODO: the json is a Struct, when it should probably be a python type.
        geojson = proto.geo.json or None
        wkt = proto.wkt.geometry or None
        if geojson is None and wkt is None:
            return None
        return Geometry(crs=crs, geojson=geojson, wkt=wkt)

    def to_proto(self):
        crs_proto = CRSProto(crs=self.crs)
        if self.geojson is not None:
            return GeometryProto(crs=crs_proto, geo=GeoJson(json=self.geojson))
        if self.wkt is not None:
            return GeometryProto(crs=crs_proto, wkt=Wkt(geometry=self.wkt))


class TextHeader:
    """A representation of text headers used to create or edit existing headers.
    
    Attributes:
        header (Optional[str]): The text content of the header
        raw_header (Optional[str]): The raw bytes of a header as a string
    """

    def __init__(self, *, header: MaybeString = None, raw_header: MaybeString = None):
        """Create a text header.

        Specify either header or raw_header.
        
        Args:
            header (str | None): The text content of a header
            raw_header (str | None): The raw bytes of a header
        """
        self.header = header
        self.raw_header = raw_header

    def __repr__(self):
        return f"TextHeader<{self.header}>"

    def from_proto(proto):
        return TextHeader(header=proto.header, raw_header=proto.raw_header)

    def into_proto(self):
        return TextHeaderProto(header=self.header, raw_header=self.raw_header)


class BinaryHeader:
    """A representation of binary headers used to create or edit existing headers.
    
    BinaryHeader.FIELDS contains the list of valid fields. to set after the object is constructed.

    Attributes:
        traces
        trace_data_type
        fixed_length_traces
        segy_revision
        auxtraces
        interval
        interval_original
        samples
        samples_original
        ensemble_fold
        vertical_sum
        trace_type_sorting_code
        sweep_type_code
        sweep_frequency_start
        sweep_frequency_end
        sweep_length
        sweep_channel
        sweep_taper_start
        sweep_taper_end
        sweep_taper_type
        correlated_traces
        amplitude_recovery
        original_measurement_system
        impulse_signal_polarity
        vibratory_polarity_code
    """

    FIELDS = (
        "traces",
        "trace_data_type",
        "fixed_length_traces",
        "segy_revision",
        "auxtraces",
        "interval",
        "interval_original",
        "samples",
        "samples_original",
        "ensemble_fold",
        "vertical_sum",
        "trace_type_sorting_code",
        "sweep_type_code",
        "sweep_frequency_start",
        "sweep_frequency_end",
        "sweep_length",
        "sweep_channel",
        "sweep_taper_start",
        "sweep_taper_end",
        "sweep_taper_type",
        "correlated_traces",
        "amplitude_recovery",
        "original_measurement_system",
        "impulse_signal_polarity",
        "vibratory_polarity_code",
    )

    def __init__(self, *args, raw_header: Union[bytes, None] = None, **kwargs):
        """Initialize.
        
        Args:
            *args (int): An optional list of arguments. The fields are assigned to the binary_header fields in sequential order, and missing fields are assigned None.
            **kwargs (int): An optional key-value mapping of arguments, which overwrite any values from *args.
            raw_header (bytes | None): Optional raw header.            
        """
        for i, field in enumerate(BinaryHeader.FIELDS):
            val = args[i] if i < len(args) else None
            val = kwargs[field] if field in kwargs else val
            setattr(self, field, val)
        self.raw_header = raw_header

    def __repr__(self):
        fields = []
        for field in self.FIELDS:
            val = getattr(self, field)
            if val is not None:
                fields.append(f"{field}: {val}")
        fields = ", ".join(fields)
        return f"BinaryHeader<{fields}>"

    @staticmethod
    def from_proto(proto) -> "BinaryHeader":
        return BinaryHeader(
            traces=proto.traces,
            trace_data_type=proto.trace_data_type,
            fixed_length_traces=proto.fixed_length_traces,
            segy_revision=proto.segy_revision,
            auxtraces=proto.auxtraces,
            interval=proto.interval,
            interval_original=proto.interval_original,
            samples=proto.samples,
            samples_original=proto.samples_original,
            ensemble_fold=proto.ensemble_fold,
            vertical_sum=proto.vertical_sum,
            trace_type_sorting_code=proto.trace_type_sorting_code,
            sweep_type_code=proto.sweep_type_code,
            sweep_frequency_start=proto.sweep_frequency_start,
            sweep_frequency_end=proto.sweep_frequency_end,
            sweep_length=proto.sweep_length,
            sweep_channel=proto.sweep_channel,
            sweep_taper_start=proto.sweep_taper_start,
            sweep_taper_end=proto.sweep_taper_end,
            sweep_taper_type=proto.sweep_taper_type,
            correlated_traces=proto.correlated_traces,
            amplitude_recovery=proto.amplitude_recovery,
            original_measurement_system=proto.original_measurement_system,
            impulse_signal_polarity=proto.impulse_signal_polarity,
            vibratory_polarity_code=proto.vibratory_polarity_code,
            raw_header=proto.raw_header,
        )

    def into_proto(self):
        return BinaryHeaderProto(
            traces=self.traces,
            trace_data_type=self.trace_data_type,
            fixed_length_traces=self.fixed_length_traces,
            segy_revision=self.segy_revision,
            auxtraces=self.auxtraces,
            interval=self.interval,
            interval_original=self.interval_original,
            samples=self.samples,
            samples_original=self.samples_original,
            ensemble_fold=self.ensemble_fold,
            vertical_sum=self.vertical_sum,
            trace_type_sorting_code=self.trace_type_sorting_code,
            sweep_type_code=self.sweep_type_code,
            sweep_frequency_start=self.sweep_frequency_start,
            sweep_frequency_end=self.sweep_frequency_end,
            sweep_length=self.sweep_length,
            sweep_channel=self.sweep_channel,
            sweep_taper_start=self.sweep_taper_start,
            sweep_taper_end=self.sweep_taper_end,
            sweep_taper_type=self.sweep_taper_type,
            correlated_traces=self.correlated_traces,
            amplitude_recovery=self.amplitude_recovery,
            original_measurement_system=self.original_measurement_system,
            impulse_signal_polarity=self.impulse_signal_polarity,
            vibratory_polarity_code=self.vibratory_polarity_code,
            raw_header=self.raw_header,
        )


class SeismicStore:
    """Represents a seismic store.
    
    Attributes:
        id (int): The unique internal id of the seismic store.
        name (str): The unique name of the seismic store. Will be changed to external-id in the future.
        survey_id (str): The survey this seismic store belongs to.
        ingestion_source (:py:class:`IngestionSource`): The source of the seismicstore.
        metadata (Mapping[str, str]): Any custom-defined metadata
        ingested_file (Optional[:py:class:`File`]): If present, the file this SeismicStore was ingested from
        inline_volume_def (Optional[:py:class:`VolumeDef`]): The inline-major volume definition for this seismic store.
        crossline_volume_def (Optional[:py:class:`VolumeDef`]): The crossline-major volume definition for this seismic store.
        coverage (Optional[:py:class:`Geometry`]): If present, the coverage geometry for this seismic store
        text_header (Optional[:py:class:`TextHeader`]): If present, the text header for this seismic store
        binary_header (Optional[:py:class:`BinaryHeader`]): If present, the binary header for this seismic store
        storage_tier_name (List[str]): The names of the storage tiers this seismic store exists in
    """

    id: int
    name: str
    survey_id: str
    ingestion_source: IngestionSource
    metadata: Mapping[str, str]
    ingested_file: Optional[File]
    inline_volume_def: Optional[VolumeDef]
    crossline_volume_def: Optional[VolumeDef]
    coverage: Geometry
    text_header: Optional[TextHeader]
    binary_header: Optional[BinaryHeader]
    storage_tier_name: List[str]

    def __init__(
        self,
        *,
        id,
        name,
        survey_id,
        ingestion_source,
        metadata,
        ingested_file,
        inline_volume_def,
        crossline_volume_def,
        coverage,
        text_header,
        binary_header,
        storage_tier_name,
    ):
        self.id = id
        self.name = name
        self.survey_id = survey_id
        self.ingestion_source = ingestion_source
        self.metadata = metadata
        self.ingested_file = ingested_file
        self.inline_volume_def = inline_volume_def
        self.crossline_volume_def = crossline_volume_def
        self.coverage = coverage
        self.text_header = text_header
        self.binary_header = binary_header
        self.storage_tier_name = storage_tier_name

    def __repr__(self):
        return f"SeismicStore<id: {self.id}, name: {self.name}, survey_id: {self.survey_id}, ingestion_source: {self.ingestion_source}, metadata: {self.metadata}, storage_tier: {self.storage_tier_name}>"

    @staticmethod
    def from_proto(proto) -> "SeismicStore":
        metadata = {}
        for key in proto.metadata:
            metadata[key] = proto.metadata[key]

        # Only decode protobuf fields that are defined.
        inline_volume_def = None
        crossline_volume_def = None
        coverage = None
        text_header = None
        binary_header = None
        if proto.HasField("inline_volume_def"):
            inline_volume_def = VolumeDef.from_proto(proto.inline_volume_def)
        if proto.HasField("crossline_volume_def"):
            crossline_volume_def = VolumeDef.from_proto(proto.crossline_volume_def)
        if proto.HasField("coverage"):
            coverage = Geometry.from_proto(proto.coverage)
        if proto.HasField("text_header"):
            text_header = TextHeader.from_proto(proto.text_header)
        if proto.HasField("binary_header"):
            binary_header = BinaryHeader.from_proto(proto.binary_header)

        return SeismicStore(
            id=proto.id,
            name=proto.name,
            survey_id=proto.survey_id,
            ingestion_source=proto.ingestion_source,
            metadata=metadata,
            ingested_file=proto.ingested_file,
            inline_volume_def=inline_volume_def,
            crossline_volume_def=crossline_volume_def,
            coverage=coverage,
            text_header=text_header,
            binary_header=binary_header,
            storage_tier_name=proto.storage_tier_name,
        )


class SeismicLineRange:
    """Represents the line range for a seismic"""

    inline_min: int
    inline_max: int
    inline_step: int
    crossline_min: int
    crossline_max: int
    crossline_step: int

    def __init__(self, inline_min, inline_max, inline_step, crossline_min, crossline_max, crossline_step):
        self.inline_min = inline_min
        self.inline_max = inline_max
        self.inline_step = inline_step
        self.crossline_min = crossline_min
        self.crossline_max = crossline_max
        self.crossline_step = crossline_step

    def __repr__(self):
        return (
            "SeismicLineRange<"
            f"inline_min: {self.inline_min}, "
            f"inline_max: {self.inline_max}, "
            f"inline_step: {self.inline_step}, "
            f"crossline_min: {self.crossline_min}, "
            f"crossline_max: {self.crossline_max}, "
            f"crossline_step: {self.crossline_step}>"
        )

    @staticmethod
    def from_proto(proto) -> "SeismicLineRange":
        return SeismicLineRange(
            inline_min=proto.inline.min.value,
            inline_max=proto.inline.max.value,
            inline_step=proto.inline.step.value,
            crossline_min=proto.crossline.min.value,
            crossline_max=proto.crossline.max.value,
            crossline_step=proto.crossline.step.value,
        )


class Seismic:
    """Represents a seismic, a cutout of a seismic store.
    
    Attributes:
        id (int): The unique internal id of the seismic
        external_id (str): The external id of the seismic
        crs (str): The Coordinate Reference System of the seismic
        metadata (Mapping[str, str]): Any custom-defined metadata
        text_header (Optional[:py:class:`TextHeader`]): The text header that corresponds to the seismic
        binary_header (Optional[:py:class:`BinaryHeader`]): The binary header that corresponds to the seismic
        line_range: TODO
        volume_def (Optional[:py:class:`VolumeDef`]): The VolumeDef describing the seismic
        partition_id (int): The id of the partition the seismic belongs to
        seismicstore_id (int): The id of the seismicstore the seismic is derived from
        coverage (Optional[:py:class:`Geometry`]): The coverage geometry for the seismic.
    """

    id: int
    external_id: str
    name: str
    crs: str
    metadata: Mapping[str, str]
    text_header: Optional[TextHeader]
    binary_header: Optional[BinaryHeader]
    line_range: Optional[SeismicLineRange]
    volume_def: Optional[VolumeDef]
    partition_id: int
    seismicstore_id: Optional[int]
    coverage: Optional[Geometry]

    def __init__(
        self,
        *,
        id,
        external_id,
        name,
        crs,
        metadata,
        text_header,
        binary_header,
        line_range,
        volume_def,
        partition_id,
        seismicstore_id,
        coverage,
    ):
        self.id = id
        self.external_id = external_id
        self.name = name
        self.crs = crs
        self.metadata = metadata
        self.text_header = text_header
        self.binary_header = binary_header
        self.line_range = line_range
        self.volume_def = volume_def
        self.partition_id = partition_id
        self.seismicstore_id = seismicstore_id
        self.coverage = coverage

    def __repr__(self):
        return f"Seismic<id: {self.id}, external_id: {self.external_id}, name: {self.name}, crs: {self.crs}, metadata: {self.metadata}>"

    @staticmethod
    def from_proto(proto) -> "Seismic":
        metadata = {}
        for key in proto.metadata:
            metadata[key] = proto.metadata[key]

        # Only decode protobuf fields that are defined.
        text_header = None
        binary_header = None
        line_range = None
        volume_def = None
        coverage = None
        if proto.HasField("text_header"):
            text_header = TextHeader.from_proto(proto.text_header)
        if proto.HasField("binary_header"):
            binary_header = BinaryHeader.from_proto(proto.binary_header)
        if proto.HasField("line_range"):
            line_range = SeismicLineRange.from_proto(proto.line_range)
        if proto.HasField("volume_def"):
            volume_def = VolumeDef.from_proto(proto.volume_def)
        if proto.HasField("coverage"):
            coverage = Geometry.from_proto(proto.coverage)

        return Seismic(
            id=proto.id,
            external_id=proto.external_id,
            name=proto.name,
            crs=proto.crs,
            metadata=metadata,
            text_header=text_header,
            binary_header=binary_header,
            line_range=line_range,
            volume_def=volume_def,
            partition_id=proto.partition_id,
            seismicstore_id=proto.seismicstore_id,
            coverage=coverage,
        )


class Partition:
    """Represents a partition and its included seismics
    
    Attributes:
        id (int): The unique internal id for this partition
        name (str): The human-friendly name for this partition
        seismics (List[:py:class:`Seismic`]): The list of seismics that belong to this partition
    """

    id: int
    external_id: str
    name: str
    seismics: List[Seismic]

    def __init__(self, *, id, external_id, name, seismics):
        self.id = id
        self.external_id = external_id
        self.name = name
        self.seismics = seismics

    def __repr__(self):
        return f"Partition<id: {self.id}, external_id: {self.external_id}, name: {self.name}>"

    @staticmethod
    def from_proto(proto) -> "Partition":
        seismics = [Seismic.from_proto(s) for s in proto.seismics]
        return Partition(id=proto.id, external_id=proto.external_id, name=proto.name, seismics=seismics)
