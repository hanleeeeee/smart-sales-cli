from src.storage import load_data, save_data
from src.customer import (
    create_customer, list_customers, get_customer,
    search_customers, update_customer, delete_customer,
    export_customers_to_csv
)
from src.report import (
    create_report, list_reports, get_report, update_report,
    submit_report, approve_report, reject_report, withdraw_report
)


DATA_DIR = 'data'
CUSTOMERS_FILE = f'{DATA_DIR}/customers.json'
SALES_REPORTS_FILE = f'{DATA_DIR}/sales_reports.json'


def _load_all():
    """모든 데이터를 로드한다."""
    customers = load_data(CUSTOMERS_FILE)
    reports = load_data(SALES_REPORTS_FILE)
    return customers, reports


def _save_all(customers, reports):
    """모든 데이터를 저장한다."""
    save_data(CUSTOMERS_FILE, customers)
    save_data(SALES_REPORTS_FILE, reports)


def _print_customer(c):
    """고객사 1건을 출력한다."""
    print(f"  ID: {c['customer_id']} | {c['customer_name']} | 담당자: {c['manager_name']} | {c['email']}")


def _print_report(r):
    """영업일지 1건을 출력한다."""
    print(f"  ID: {r['report_id']} | 고객사: {r['customer_id']} | {r['activity_date']} | {r['status']}")
    print(f"  내용: {r['content']}")


def export_csv_menu():
    """고객사 목록 CSV 내보내기"""
    customers, reports = _load_all()

    print('\n' + '=' * 50)
    print('CSV 내보내기')
    print('=' * 50)

    if not customers:
        print('내보낼 고객사 데이터가 없습니다.')
        return customers, reports

    filepath, err = export_customers_to_csv(customers)
    if err:
        print(f'오류: {err}')
    else:
        print(f'고객사 목록이 CSV 파일로 내보내졌습니다.')
        print(f'  파일: {filepath}')

    print()
    input('Enter를 누르면 메인 메뉴로 돌아갑니다.')
    return customers, reports


def customer_menu():
    """고객사 관리 서브메뉴"""
    customers, reports = _load_all()

    while True:
        print('\n' + '=' * 50)
        print('고객사 관리')
        print('=' * 50)
        print('1. 고객사 등록')
        print('2. 고객사 목록')
        print('3. 고객사 상세 조회')
        print('4. 고객사 검색')
        print('5. 고객사 수정')
        print('6. 고객사 삭제')
        print('7. 뒤로 가기')
        print('=' * 50)

        choice = input('선택: ').strip()

        if choice == '1':
            print('\n[고객사 등록]')
            name = input('고객사명: ').strip()
            manager = input('담당자명: ').strip()
            email = input('이메일: ').strip()
            customers, err = create_customer(customers, name, manager, email)
            if err:
                print(f'오류: {err}')
            else:
                print('등록되었습니다.')
            _save_all(customers, reports)

        elif choice == '2':
            print('\n[고객사 목록]')
            result = list_customers(customers)
            if not result:
                print('등록된 고객사가 없습니다.')
            else:
                for c in result:
                    _print_customer(c)

        elif choice == '3':
            print('\n[고객사 상세 조회]')
            customer_id = input('고객사 ID: ').strip()
            c = get_customer(customers, customer_id)
            if c:
                _print_customer(c)
            else:
                print('존재하지 않는 고객사입니다.')

        elif choice == '4':
            print('\n[고객사 검색]')
            keyword = input('검색어: ').strip()
            result = search_customers(customers, keyword)
            if not result:
                print('검색 결과가 없습니다.')
            else:
                for c in result:
                    _print_customer(c)

        elif choice == '5':
            print('\n[고객사 수정]')
            customer_id = input('고객사 ID: ').strip()
            c = get_customer(customers, customer_id)
            if not c:
                print('존재하지 않는 고객사입니다.')
                continue
            print(f'기존 정보: {c["customer_name"]} / {c["manager_name"]} / {c["email"]}')
            name = input('새 고객사명: ').strip()
            manager = input('새 담당자명: ').strip()
            email = input('새 이메일: ').strip()
            customers, err = update_customer(customers, customer_id, name, manager, email)
            if err:
                print(f'오류: {err}')
            else:
                print('수정되었습니다.')
            _save_all(customers, reports)

        elif choice == '6':
            print('\n[고객사 삭제]')
            customer_id = input('고객사 ID: ').strip()
            customers, err = delete_customer(customers, customer_id)
            if err:
                print(f'오류: {err}')
            else:
                print('삭제되었습니다.')
            _save_all(customers, reports)

        elif choice == '7':
            break

        else:
            print('잘못된 선택입니다. 다시 입력해주세요.')

    return customers, reports


def report_menu():
    """영업일지 관리 서브메뉴"""
    customers, reports = _load_all()

    while True:
        print('\n' + '=' * 50)
        print('영업일지 관리')
        print('=' * 50)
        print('1. 영업일지 등록')
        print('2. 영업일지 목록')
        print('3. 영업일지 수정')
        print('4. 영업일지 상신')
        print('5. 영업일지 승인')
        print('6. 영업일지 반려')
        print('7. 영업일지 회수')
        print('8. 뒤로 가기')
        print('=' * 50)

        choice = input('선택: ').strip()

        if choice == '1':
            print('\n[영업일지 등록]')
            customer_id = input('고객사 ID: ').strip()
            activity_date = input('활동일자 (YYYY-MM-DD): ').strip()
            content = input('활동 내용: ').strip()
            reports, err = create_report(reports, customer_id, activity_date, content)
            if err:
                print(f'오류: {err}')
            else:
                print('등록되었습니다.')
            _save_all(customers, reports)

        elif choice == '2':
            print('\n[영업일지 목록]')
            result = list_reports(reports)
            if not result:
                print('등록된 영업일지가 없습니다.')
            else:
                for r in result:
                    _print_report(r)

        elif choice == '3':
            print('\n[영업일지 수정]')
            report_id = input('영업일지 ID: ').strip()
            r = get_report(reports, report_id)
            if not r:
                print('존재하지 않는 영업일지입니다.')
                continue
            print(f'기존 정보: {r["activity_date"]} / {r["content"]} (상태: {r["status"]})')
            activity_date = input('새 활동일자 (YYYY-MM-DD): ').strip()
            content = input('새 활동 내용: ').strip()
            reports, err = update_report(reports, report_id, activity_date, content)
            if err:
                print(f'오류: {err}')
            else:
                print('수정되었습니다.')
            _save_all(customers, reports)

        elif choice == '4':
            print('\n[영업일지 상신]')
            report_id = input('영업일지 ID: ').strip()
            reports, err = submit_report(reports, report_id)
            if err:
                print(f'오류: {err}')
            else:
                print('상신되었습니다.')
            _save_all(customers, reports)

        elif choice == '5':
            print('\n[영업일지 승인]')
            report_id = input('영업일지 ID: ').strip()
            reports, err = approve_report(reports, report_id)
            if err:
                print(f'오류: {err}')
            else:
                print('승인되었습니다.')
            _save_all(customers, reports)

        elif choice == '6':
            print('\n[영업일지 반려]')
            report_id = input('영업일지 ID: ').strip()
            reports, err = reject_report(reports, report_id)
            if err:
                print(f'오류: {err}')
            else:
                print('반려되었습니다.')
            _save_all(customers, reports)

        elif choice == '7':
            print('\n[영업일지 회수]')
            report_id = input('영업일지 ID: ').strip()
            reports, err = withdraw_report(reports, report_id)
            if err:
                print(f'오류: {err}')
            else:
                print('회수되었습니다.')
            _save_all(customers, reports)

        elif choice == '8':
            break

        else:
            print('잘못된 선택입니다. 다시 입력해주세요.')

    return customers, reports


def summary_menu():
    """고객사별 활동 요약"""
    customers, reports = _load_all()

    print('\n' + '=' * 50)
    print('고객사별 활동 요약')
    print('=' * 50)

    if not customers:
        print('등록된 고객사가 없습니다.')
        return customers, reports

    for c in customers:
        cid = c['customer_id']
        related = [r for r in reports if r['customer_id'] == cid]
        total = len(related)
        draft = sum(1 for r in related if r['status'] == 'DRAFT')
        submitted = sum(1 for r in related if r['status'] == 'SUBMITTED')
        approved = sum(1 for r in related if r['status'] == 'APPROVED')
        rejected = sum(1 for r in related if r['status'] == 'REJECTED')

        print(f'\n[{cid}] {c["customer_name"]} (담당자: {c["manager_name"]})')
        print(f'  총 영업일지: {total}건')
        if total > 0:
            print(f'  DRAFT: {draft}건 | SUBMITTED: {submitted}건 | APPROVED: {approved}건 | REJECTED: {rejected}건')

    print()
    input('Enter를 누르면 메인 메뉴로 돌아갑니다.')
    return customers, reports