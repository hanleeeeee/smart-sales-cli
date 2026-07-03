import re
import datetime
from src.storage import load_data


DATA_DIR = 'data'
CUSTOMERS_FILE = f'{DATA_DIR}/customers.json'

VALID_STATUSES = ['DRAFT', 'SUBMITTED', 'APPROVED', 'REJECTED']


def _generate_report_id(reports):
    """영업일지 ID를 자동 생성한다. (R001, R002, ...)"""
    max_num = 0
    for r in reports:
        rid = r.get('report_id', '')
        if rid.startswith('R') and rid[1:].isdigit():
            num = int(rid[1:])
            if num > max_num:
                max_num = num
    return f'R{max_num + 1:03d}'


def _validate_date(date_str):
    """날짜가 YYYY-MM-DD 형식이고 실제 존재하는 날짜인지 검증한다."""
    if not date_str or not date_str.strip():
        return '활동일자를 입력해주세요.'
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str.strip()):
        return '날짜 형식은 YYYY-MM-DD로 입력해주세요.'
    try:
        datetime.datetime.strptime(date_str.strip(), '%Y-%m-%d')
    except ValueError:
        return '존재하지 않는 날짜입니다.'
    return None


def _validate_customer_id(customer_id):
    """고객사 ID가 customers.json에 존재하는지 확인한다."""
    if not customer_id or not customer_id.strip():
        return '고객사 ID를 입력해주세요.'
    customers = load_data(CUSTOMERS_FILE)
    for c in customers:
        if c.get('customer_id') == customer_id.strip():
            return None
    return '존재하지 않는 고객사입니다.'


def _validate_content(content):
    """활동 내용을 검증한다."""
    if not content or not content.strip():
        return '활동 내용을 입력해주세요.'
    return None


def create_report(reports, customer_id, activity_date, content):
    """새 영업일지를 등록한다. (상태: DRAFT)

    Returns:
        (수정된 reports 리스트, 오류 메시지)
        성공 시 오류 메시지는 None.
    """
    err = _validate_customer_id(customer_id)
    if err:
        return reports, err

    err = _validate_date(activity_date)
    if err:
        return reports, err

    err = _validate_content(content)
    if err:
        return reports, err

    new_report = {
        'report_id': _generate_report_id(reports),
        'customer_id': customer_id.strip(),
        'activity_date': activity_date.strip(),
        'content': content.strip(),
        'status': 'DRAFT'
    }
    reports.append(new_report)
    return reports, None


def list_reports(reports):
    """전체 영업일지 목록을 반환한다."""
    return list(reports)


def get_report(reports, report_id):
    """ID로 영업일지 1건을 조회한다. 없으면 None 반환."""
    for r in reports:
        if r.get('report_id') == report_id:
            return r
    return None


def update_report(reports, report_id, activity_date, content):
    """영업일지를 수정한다. (DRAFT 상태에서만 가능)

    Returns:
        (수정된 reports 리스트, 오류 메시지)
        성공 시 오류 메시지는 None.
    """
    err = _validate_date(activity_date)
    if err:
        return reports, err

    err = _validate_content(content)
    if err:
        return reports, err

    for r in reports:
        if r.get('report_id') == report_id:
            if r.get('status') != 'DRAFT':
                return reports, 'DRAFT 상태에서만 수정할 수 있습니다.'
            r['activity_date'] = activity_date.strip()
            r['content'] = content.strip()
            return reports, None

    return reports, '존재하지 않는 영업일지입니다.'


def _transition_status(reports, report_id, action, valid_from, target_status):
    """상태 전이를 수행한다. (내부 헬퍼)"""
    for r in reports:
        if r.get('report_id') == report_id:
            if r.get('status') not in valid_from:
                valid_str = ', '.join(valid_from)
                return reports, f'{valid_str} 상태에서만 {action}할 수 있습니다.'
            r['status'] = target_status
            return reports, None
    return reports, '존재하지 않는 영업일지입니다.'


def submit_report(reports, report_id):
    """영업일지를 상신한다. (DRAFT → SUBMITTED)"""
    return _transition_status(reports, report_id, '상신', ['DRAFT'], 'SUBMITTED')


def approve_report(reports, report_id):
    """영업일지를 승인한다. (SUBMITTED → APPROVED)"""
    return _transition_status(reports, report_id, '승인', ['SUBMITTED'], 'APPROVED')


def reject_report(reports, report_id):
    """영업일지를 반려한다. (SUBMITTED → REJECTED)"""
    return _transition_status(reports, report_id, '반려', ['SUBMITTED'], 'REJECTED')


def withdraw_report(reports, report_id):
    """영업일지를 회수한다. (SUBMITTED → DRAFT)"""
    return _transition_status(reports, report_id, '회수', ['SUBMITTED'], 'DRAFT')
