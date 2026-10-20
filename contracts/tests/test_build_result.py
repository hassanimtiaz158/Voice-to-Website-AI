from contracts.build_result import BuildResultContract


def test_build_result_contract_defaults():
    res = BuildResultContract(success=True)
    assert res.success is True
    assert res.exit_code == 0
    assert res.tsc_passed is False
    assert res.lint_passed is False
    assert res.build_passed is False
    assert res.playwright_passed is False
    assert res.failing_files == []
    assert res.raw_error_log is None
    assert res.preview_url is None
    assert res.screenshot_s3_key is None


def test_build_result_contract_failure_payload():
    res = BuildResultContract(
        success=False,
        exit_code=1,
        tsc_passed=False,
        lint_passed=True,
        build_passed=False,
        playwright_passed=False,
        failing_files=["src/components/Hero.tsx"],
        raw_error_log="src/components/Hero.tsx(12,5): error TS2304: Cannot find name 'LucideIcon'.",
    )
    assert res.success is False
    assert res.exit_code == 1
    assert len(res.failing_files) == 1
    assert "TS2304" in (res.raw_error_log or "")

    # Ensure JSON serialization round-trip
    serialized = res.model_dump_json()
    reconstructed = BuildResultContract.model_validate_json(serialized)
    assert reconstructed == res
