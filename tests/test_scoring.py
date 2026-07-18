from pipelines.scoring import clamp, normalized_alert_score


def test_clamp_limits_values():
    assert clamp(-0.5) == 0.0
    assert clamp(0.4) == 0.4
    assert clamp(1.5) == 1.0


def test_normalized_alert_score_uses_shared_scale():
    assert normalized_alert_score(0, 0) == 60.0
    assert normalized_alert_score(0.5, 0.5) == 80.0
    assert normalized_alert_score(10, 10) == 100.0
