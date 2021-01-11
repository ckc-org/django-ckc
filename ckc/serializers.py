class DefaultUserCreateMixin:
    """This will automatically set `YourModel.created_by` to `request.user`. To override which
    attribute the user is written to, add a `user_field` to your classes Meta information
    Example:
        class YourModel(models.Model):
            owner = models.ForeignKey(User, on_delete=models.CASCADE)

        class MySerializer(DefaultUserCreateMixin, ModelSerializer):
            class Meta:
                model = YourModel
                # YourModel.owner = a foreign key to request.user which differs from the
                # default `created_by`
                user_field = 'owner'
    """
    def create(self, validated_data):
        # get name of the user field we'll be writing request.user to, default created_by
        user_field = getattr(self.Meta, 'user_field', 'created_by')

        assert hasattr(self.Meta.model, user_field), f"{self.Meta.model} needs to have field {user_field} so " \
                                                     f"DefaultUserCreateMixin can write to it"

        if user_field not in validated_data:
            if 'request' not in self.context:
                raise Exception('self.context does not contain "request". Have you overwritten get_serializer_context '
                                'and overwrote context?')
            validated_data[user_field] = self.context['request'].user
        return super().create(validated_data)
