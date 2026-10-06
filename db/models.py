from mongoengine import CASCADE, Document, ListField, ReferenceField, StringField


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author, required=True, reverse_delete_rule=CASCADE)
    quote = StringField(required=True)

    meta = {"collection": "quotes", "indexes": ["tags", "author"]}
