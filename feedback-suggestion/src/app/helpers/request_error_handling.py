from fastapi import HTTPException


def check_artemis_response(response):
    if not response.ok:
        print("Error with status code", response.status_code)
        raise HTTPException(status_code=response.status_code, detail="Error on Artemis server: " + response.text)


def check_assessment_response(response):
    if response.status_code == 404:
        raise HTTPException(status_code=404,
                            detail="No result found for assessment. Assessment might not be submitted.")
    check_artemis_response(response)