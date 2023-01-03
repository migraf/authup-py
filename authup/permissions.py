from authup.schemas import TokenIntrospectionResponse, UserPermission


def check_permissions(
    token_introspection: TokenIntrospectionResponse,
    required_permissions: list[UserPermission],
) -> bool:
    """
    Check if a token has the required permissions
    :param token_introspection:
    :param required_permissions:
    :return:
    """
    if not required_permissions:
        return True

    if not token_introspection.permissions:
        return False

    return _check_permissions(token_introspection.permissions, required_permissions)


def _check_permissions(
    token_permissions: list[UserPermission],
    required_permissions: list[UserPermission],
) -> bool:
    """
    Compare the required permissions with the token permissions, taking inverse and power into account
    :param token_permissions:
    :param token_permissions:
    :return:
    """

    token_perm_dict = {p.target: p for p in token_permissions}

    for required_permission in required_permissions:
        # the required permission is not in the token permissions
        if required_permission.target not in token_perm_dict:
            return False

        # check for inverse and compare power
        token_permission = token_perm_dict[required_permission.target]
        if token_permission.inverse:
            if token_permission.power >= required_permission.power:
                return False
        else:
            if token_permission.power < required_permission.power:
                return False

        # check condition
        # todo: implement condition check

    return True