from typing import BinaryIO
from dataclasses import dataclass, field 
import io

from ..abstract_request import AbstractRequest
from ...utils.converter import (
    decode_compact_array, 
    decode_int32, 
    decode_tagged_fields,
    decode_compact_string,
    encode_compact_string,
    encode_int32,
    encode_tagged_fields
    )


@dataclass
class DescribeTopicPartitionsRequestTopic:
    name : str
    
    @classmethod
    def decode(cls, buffer : BinaryIO):
        item = DescribeTopicPartitionsRequestTopic(
            name = decode_compact_string(buffer)
        )
        decode_tagged_fields(buffer)
        return item
        


@dataclass
class DescribeTopicPartitionsCursor:
    topic_name : str
    partition_index : int 

    @classmethod
    def decode(cls, buffer: BinaryIO):
         
        if buffer.read(1) == b"\xff":
            return None
        buffer.seek(-1, io.SEEK_CUR)

        cursor = DescribeTopicPartitionsCursor(
            topic_name=decode_compact_string(buffer),
            partition_index=decode_int32(buffer),
        )
        decode_tagged_fields(buffer)
        return cursor

    def encode(self):
        return b"".join([
            encode_compact_string(self.topic_name),
            encode_int32(self.partition_index),
            encode_tagged_fields(),
        ])
@dataclass
class DescribeTopicPartitionsRequest(AbstractRequest):
    
    topics: list[DescribeTopicPartitionsRequestTopic] 
    response_partition_limit: int 
    cursor: DescribeTopicPartitionsCursor | None = None

    @classmethod
    def decode_body(cls, request_buffer: BinaryIO):

        request_body = {
            "topics": decode_compact_array(request_buffer, DescribeTopicPartitionsRequestTopic.decode),
            "response_partition_limit": decode_int32(request_buffer),
            "cursor": DescribeTopicPartitionsCursor.decode(request_buffer),
        }
        decode_tagged_fields(request_buffer)
        return request_body