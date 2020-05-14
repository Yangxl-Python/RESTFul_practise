from rest_framework import serializers

from book.models import Books, Press


class PressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Press
        fields = ('id', 'address')


class BooksViewSerializer(serializers.ModelSerializer):

    publish = PressSerializer()

    class Meta:
        model = Books
        # fields = '__all__'
        fields = ('book_name', 'price', 'authors_name', 'publish_name', 'publish')
        # exclude = ('')
        # depth = 1


class BooksViewDeserializer(serializers.ModelSerializer):
    def validate_book_name(self, value):
        if 'A' in value:
            raise serializers.ValidationError('《A》已存在')
        return value

    def validate(self, attrs):
        book_obj = Books.objects.filter(book_name=attrs.get('book_name'),
                                        publish=attrs.get('publish'))
        if book_obj:
            raise serializers.ValidationError('该出版社已经发布过该图书')
        return attrs

    class Meta:
        model = Books
        fields = '__all__'
        extra_kwargs = {
            'book_name': {
                'required': True,
                'min_length': 2,
                'error_messages': {
                    'required': '该字段不能为空',
                    'min_length': '最小长度大于2'
                }
            }
        }


class BooksViewSerializerV2(serializers.ModelSerializer):
    def validate_book_name(self, value):
        if 'A' in value:
            raise serializers.ValidationError('《A》已存在')
        return value

    def validate(self, attrs):
        book_obj = Books.objects.filter(book_name=attrs.get('book_name'),
                                        publish=attrs.get('publish'))
        if book_obj:
            raise serializers.ValidationError('该出版社已经发布过该图书')
        return attrs

    class Meta:
        model = Books
        fields = ('book_name', 'price', 'authors_info', 'publish_name', 'publish', 'authors')
        extra_kwargs = {
            'book_name': {
                'required': True,
                'min_length': 2,
                'error_messages': {
                    'required': '该字段不能为空',
                    'min_length': '最小长度大于2'
                }
            },
            'authors_name': {
                'read_only': True
            },
            'publish_name': {
                'read_only': True
            },
            'authors': {
                'write_only':True
            }
        }
