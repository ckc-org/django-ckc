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
        user_field = getattr(self.Meta, 'user_field', 'created_by')
        if user_field not in validated_data:
            if 'request' not in self.context:
                raise Exception('self.context does not contain "request". Have you overwritten get_serializer_context?')
            validated_data[user_field] = self.context['request'].user
        return super().create(validated_data)
