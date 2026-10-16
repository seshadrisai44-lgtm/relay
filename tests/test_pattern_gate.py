from gate.pattern_gate import check_note


def test_safe_note_is_allowed():
    result = check_note("Project update: completed the design review.")
    assert result["allowed"] is True


def test_email_address_is_blocked():
    result = check_note("Contact: test@example.com")
    assert result["allowed"] is False
    assert "PG-03" in result["findings"]


def test_secret_like_value_is_blocked():
    result = check_note("API_KEY = fake_test_value")
    assert result["allowed"] is False
    assert "PG-05" in result["findings"]


def test_invalid_input_is_not_allowed():
    result = check_note(None)
    assert result["allowed"] is False


def test_empty_input_is_allowed_to_be_checked():
    result = check_note("")
    assert result["allowed"] is True


def test_ip_address_is_blocked():
    result = check_note("Server address: 192.0.2.10")
    assert result["allowed"] is False
    assert "PG-01" in result["findings"]


def test_internal_server_name_is_blocked():
    result = check_note("Server: SRV-PROD-01")
    assert result["allowed"] is False
    assert "PG-02" in result["findings"]


def test_url_is_blocked():
    result = check_note("Internal link: https://portal.example.com/status")
    assert result["allowed"] is False
    assert "PG-03" in result["findings"]


def test_service_account_is_blocked():
    result = check_note(r"Account: CORP\svc_backup")
    assert result["allowed"] is False
    assert "PG-04" in result["findings"]


def test_password_like_value_is_blocked():
    result = check_note("PASSWORD: fake_demo_value")
    assert result["allowed"] is False
    assert "PG-05" in result["findings"]


def test_mac_address_is_blocked():
    result = check_note("Device MAC: 00:1A:2B:3C:4D:5E")
    assert result["allowed"] is False
    assert "PG-06" in result["findings"]


def test_incident_ticket_id_is_blocked():
    result = check_note("Incident: INC12345")
    assert result["allowed"] is False
    assert "PG-07" in result["findings"]


def test_denylisted_company_name_is_blocked():
    result = check_note("Customer: examplecorp")
    assert result["allowed"] is False
    assert "PG-08" in result["findings"]


def test_person_name_is_blocked():
    result = check_note("Assigned to: Maria Lopez")
    assert result["allowed"] is False
    assert "PG-09" in result["findings"]


def test_cve_vulnerability_id_is_blocked():
    result = check_note("Vulnerability: CVE-2024-12345")
    assert result["allowed"] is False
    assert "PG-10" in result["findings"]


def test_safe_text_without_ip_address_is_allowed():
    result = check_note("The design review is complete.")
    assert result["allowed"] is True
    assert "PG-01" not in result["findings"]


def test_safe_text_without_server_name_is_allowed():
    result = check_note("The weekly project meeting is scheduled.")
    assert result["allowed"] is True
    assert "PG-02" not in result["findings"]


def test_safe_text_without_email_or_url_is_allowed():
    result = check_note("The project review is scheduled for Monday.")
    assert result["allowed"] is True
    assert "PG-03" not in result["findings"]


def test_safe_text_without_service_account_is_allowed():
    result = check_note("The team completed the weekly report.")
    assert result["allowed"] is True
    assert "PG-04" not in result["findings"]


def test_safe_text_without_secret_is_allowed():
    result = check_note("The deployment review is complete.")
    assert result["allowed"] is True
    assert "PG-05" not in result["findings"]


def test_safe_text_without_mac_or_hash_is_allowed():
    result = check_note("The device inspection is complete.")
    assert result["allowed"] is True
    assert "PG-06" not in result["findings"]


def test_safe_text_without_ticket_id_is_allowed():
    result = check_note("The team reviewed the open tasks.")
    assert result["allowed"] is True
    assert "PG-07" not in result["findings"]


def test_safe_text_without_denylisted_name_is_allowed():
    result = check_note("The project review is complete.")
    assert result["allowed"] is True
    assert "PG-08" not in result["findings"]


def test_safe_text_without_person_name_is_allowed():
    result = check_note("The engineering team finished testing.")
    assert result["allowed"] is True
    assert "PG-09" not in result["findings"]


def test_safe_text_without_cve_is_allowed():
    result = check_note("The security review is complete.")
    assert result["allowed"] is True
    assert "PG-10" not in result["findings"]


def test_private_ip_address_is_blocked():
    result = check_note("Server IP: 10.20.30.40")
    assert result["allowed"] is False
    assert "PG-01" in result["findings"]


def test_network_range_is_blocked():
    result = check_note("Network range: 192.0.2.0/24")
    assert result["allowed"] is False
    assert "PG-01" in result["findings"]


def test_internal_corp_hostname_is_blocked():
    result = check_note("Host: app01.corp")
    assert result["allowed"] is False
    assert "PG-02" in result["findings"]


def test_domain_controller_name_is_blocked():
    result = check_note("Server: DC01")
    assert result["allowed"] is False
    assert "PG-02" in result["findings"]
