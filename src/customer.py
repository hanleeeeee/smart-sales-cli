import re
from src.storage import load_data


DATA_DIR = 'data'
SALES_REPORTS_FILE = f'{DATA_DIR}/sales_reports.json'


def _generate_customer_id(customers):
    """고객사 ID를 자동 생성한다. (C001, C002, ...)"""
    max_num = 0
    for c in customers:
        cid = c.get('customer_id', '')
        if cid.startswith('C') and cid[1:].isdigit():
            num = int(cid[1:])
            if num > max_num:
                max_num = num
    return f'C{max_num + 1:03d}'


def _validate_input(name, manager, email):
    """입력값을 검증하고 오류 메시지를 반환한다. (오류 없으면 None)"""
    if not name or not name.strip():
        return '고객사명을 입력해주세요.'
    if not manager or not manager.strip():
        return '담당자명을 입력해주세요.'
    if not email or not email.strip():
        return '이메일을 입력해주세요.'
    if '@' not in email:
        return '올바른 이메일 형식이 아닙니다.'
    return None


def _is_duplicate_email(customers, email, exclude_id=None):
    """동일한 이메일이 이미 존재하는지 확인한다."""
    for c in customers:
        if c.get('email') == email:
            if exclude_id is None or c.get('customer_id') != exclude_id:
                return True
    return False


def create_customer(customers, name, manager, email):
    """새 고객사를 등록한다.

    Returns:
        (수정된 customers 리스트, 오류 메시지)
        성공 시 오류 메시지는 None.
    """
    err = _validate_input(name, manager, email)
    if err:
        return customers, err

    if _is_duplicate_email(customers, email):
        return customers, '이미 등록된 이메일입니다.'

    new_customer = {
        'customer_id': _generate_customer_id(customers),
        'customer_name': name.strip(),
        'manager_name': manager.strip(),
        'email': email.strip()
    }
    customers.append(new_customer)
    return customers, None


def list_customers(customers):
    """전체 고객사 목록을 반환한다."""
    return list(customers)


def get_customer(customers, customer_id):
    """ID로 고객사 1건을 조회한다. 없으면 None 반환."""
    for c in customers:
        if c.get('customer_id') == customer_id:
            return c
    return None


def search_customers(customers, keyword):
    """고객사명 또는 담당자명으로 부분 일치 검색한다."""
    if not keyword or not keyword.strip():
        return list(customers)
    kw = keyword.strip().lower()
    results = []
    for c in customers:
        if kw in c.get('customer_name', '').lower() or kw in c.get('manager_name', '').lower():
            results.append(c)
    return results


def update_customer(customers, customer_id, name, manager, email):
    """고객사 정보를 수정한다.

    Returns:
        (수정된 customers 리스트, 오류 메시지)
        성공 시 오류 메시지는 None.
    """
    err = _validate_input(name, manager, email)
    if err:
        return customers, err

    if _is_duplicate_email(customers, email, exclude_id=customer_id):
        return customers, '이미 등록된 이메일입니다.'

    for c in customers:
        if c.get('customer_id') == customer_id:
            c['customer_name'] = name.strip()
            c['manager_name'] = manager.strip()
            c['email'] = email.strip()
            return customers, None

    return customers, '존재하지 않는 고객사입니다.'


def export_customers_to_csv(customers, export_dir='exports'):
    """고객사 목록을 CSV 파일로 내보낸다.

    Returns:
        (저장된 파일 경로, 오류 메시지)
        성공 시 오류 메시지는 None.
    """
    import csv
    import os
    from datetime import datetime

    if not os.path.exists(export_dir):
        try:
            os.makedirs(export_dir)
        except OSError as e:
            return None, f'CSV 저장 폴더를 생성할 수 없습니다: {e}'

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'customers_{timestamp}.csv'
    filepath = os.path.join(export_dir, filename)

    try:
        with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['customer_id', 'customer_name', 'manager_name', 'email'])
            for c in customers:
                writer.writerow([
                    c.get('customer_id', ''),
                    c.get('customer_name', ''),
                    c.get('manager_name', ''),
                    c.get('email', '')
                ])
        return filepath, None
    except IOError as e:
        return None, f'CSV 파일 저장 중 오류 발생: {e}'


def delete_customer(customers, customer_id):
    """고객사를 삭제한다. 영업일지가 있으면 삭제 불가.

    Returns:
        (수정된 customers 리스트, 오류 메시지)
        성공 시 오류 메시지는 None.
    """
    # 해당 고객사의 영업일지가 있는지 확인
    reports = load_data(SALES_REPORTS_FILE)
    for r in reports:
        if r.get('customer_id') == customer_id:
            return customers, '해당 고객사의 영업일지가 존재하여 삭제할 수 없습니다.'

    for i, c in enumerate(customers):
        if c.get('customer_id') == customer_id:
            customers.pop(i)
            return customers, None
    #DD
    return customers, '존재하지 않는 고객사입니다.'