from google.cloud import storage


def delete_model(idUsers: str, path: str) -> None:
    client = storage.Client()
    bucket = client.get_bucket("icarus-gcp.appspot.com")
    # file_path = f"PPO_hand_prosthesis_model.zip"
    idUsers = idUsers.replace('/', '\\')
    blob = bucket.blob(f"{idUsers}/{path}")
    blob.delete()
