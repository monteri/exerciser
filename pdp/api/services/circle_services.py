from pdp.api.serializers import CircleOut


def get_circle_with_children(circle):
    # Convert circle object to CircleOut model
    circle_data = CircleOut(
        id=circle.id,
        name=circle.name,
        description=circle.description,
        parent_id=circle.parent_id,
        status=circle.status,
        user_id=circle.user.id,
        depth=circle.depth,
        children=[],
    )

    # Populate the children list recursively
    for child in circle.children.all():
        circle_data.children.append(get_circle_with_children(child))

    return circle_data
