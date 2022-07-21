import json
import asyncio


# class MutateMixins:
#     @classmethod
#     def yield_data(cls, data=None):
#         if data is not None:
#             for i in data:
#                 yield i
#
#     @classmethod
#     def mutate(cls, func, mutation_type, file):
#         with open(file, 'r') as inf:
#             data = json.load(inf)
#
#         for x in cls.yield_data(data):
#             asyncio.run(func(mutation_type, x))


class MutateMixins:
    @classmethod
    def mutate(cls, func, mutation_type, file):
        with open(file, 'r') as inf:
            data = json.load(inf)
            asyncio.run(func(mutation_type, data))

    @classmethod
    def bulk_mutate(cls, func, mutation_type, file):
        with open(file, 'r') as inf:
            data = json.load(inf)
            asyncio.run(func(data, mutation_type))
