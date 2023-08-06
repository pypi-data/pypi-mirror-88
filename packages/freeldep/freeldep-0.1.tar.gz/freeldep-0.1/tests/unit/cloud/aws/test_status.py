from cli.cloud.aws.status import StackStatus

def test_success():
    assert StackStatus.success("CREATE_COMPLETE") == True
    assert StackStatus.success("UPDATE_COMPLETE") == True
    assert StackStatus.success("DELETE_COMPLETE") == True
    assert StackStatus.success("CREATE_FAILED") == False

def test_failed():
    assert StackStatus.failed("DELETE_FAILED") == True
    assert StackStatus.failed("CREATE_FAILED") == True
    assert StackStatus.failed("ROLLBACK_COMPLETE") == True
    assert StackStatus.failed("UPDATE_ROLLBACK_COMPLETE") == True
    assert StackStatus.failed("DELETE_COMPLETE") == False
