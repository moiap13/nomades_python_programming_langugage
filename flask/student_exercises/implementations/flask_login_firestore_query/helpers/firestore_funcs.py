from firebase_admin.firestore import DocumentReference, DocumentSnapshot
from firebase_admin.firestore import client


from .errors import UserNotFoundError


def get_user_by_uid(
    uid: str, firestore_connector: client, users_collection="users"
) -> dict[str, str | int]:
    """
    Get a user by their uid

    Get all the records from the collections parameter collection from firestore and loop for finding the wanted user

    Args:
        uid (str): The uid of the user
        firestore_connector (client): The firestore client for communicating with database
        users_collection (str, optional): The collection name. Defaults to "users".

    Returns:
        dict[str, str] | None: The user's data

    Raises:
        UserNotFoundError: If the user is not found
    """
    print(firestore_connector)
    users: list[DocumentSnapshot] = firestore_connector.collection(
        users_collection
    ).stream()

    for user in users:
        user_data: dict[str, str | int] = user.to_dict()
        if user_data.get("uid", "") == uid:
            user_data.update({"id": user.id})
            return user_data
    raise UserNotFoundError(
        f"The user with uid={uid} not found in collection={users_collection}"
    )
