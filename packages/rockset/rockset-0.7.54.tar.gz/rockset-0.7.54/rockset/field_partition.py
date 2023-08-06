"""
Introduction
------------

FieldPartition objects allow you to specify partitioning on your collection at creation time.

For more information on field partitions, refer to `the official documentation <https://docs.rockset.com/>`_.

Example of basic field partitions
------------------------------
::

    from rockset import Client

    rs = Client()

    partitions = [
        rs.FieldPartition.partition(
            field_name="country",
            partition_type="AUTO"
        ),
        rs.FieldPartition.partition(
            field_name="occupation",
            partition_type="AUTO"
        )
    ]

    # Create a collection partitioned on (country, occupation)
    collection = rs.Collection.create(name="collection", field_partitions=partitions)

"""


class FieldPartition(object):
    def __str__(self):
        return str(vars(self))

    def __iter__(self):
        for k, v in vars(self).items():
            yield (k, v)

    @classmethod
    def partition(cls, field_name, partition_type):
        """Creates a new partition field

        Args:
            field_name(str): Name of the field to partition on
            partition_type(str): The type of partitioning scheme to apply to
              this field. Currently supported values: ['AUTO']
        """

        return Partition(field_name, partition_type)


class Partition(FieldPartition):
    def __init__(self, field_name, partition_type):
        self.field_name = field_name
        self.type = partition_type
