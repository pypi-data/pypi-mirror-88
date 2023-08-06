

def test_download_model(test_env, afs_models, model, delete_mr_and_model, model_repository_name):
    resp = afs_models.download_model(
        save_path="download_model.h5",
        model_repository_name=model_repository_name,
        model_name="test_model",
    )
    assert resp == True
    with open("download_model.h5", "r") as f:
        content = f.read()
    assert content == "unit test"
