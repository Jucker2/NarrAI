import json

class JsonSerializer:
    @staticmethod
    def serialize(obj,indent=4):

        return json.dumps(
            obj.to_dict()
            ensure_ascii=False,
            indent=indent
        )

    @staticmethod
    def save(obj,path):
        whith open(path,"w",encoding="utf-8") as file:
        file.write(JsonSerializer.serialize(obj))

