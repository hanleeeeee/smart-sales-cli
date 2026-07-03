import unittest
from src.report import (
    create_report, list_reports, get_report, update_report,
    submit_report, approve_report, reject_report, withdraw_report
)
from src.storage import save_data


class TestReportCreate(unittest.TestCase):

    def setUp(self):
        self.reports = []
        # 테스트용 고객사 데이터 준비
        save_data('data/customers.json', [
            {'customer_id': 'C001', 'customer_name': '테스트사', 'manager_name': '홍길동', 'email': 'hong@test.com'}
        ])

    def tearDown(self):
        save_data('data/customers.json', [])
        save_data('data/sales_reports.json', [])

    def test_create_normal(self):
        """정상 등록 시 report_id가 R001, 상태는 DRAFT이다."""
        reports, err = create_report(self.reports, 'C001', '2026-06-09', '제품 소개 미팅')
        self.assertIsNone(err)
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0]['report_id'], 'R001')
        self.assertEqual(reports[0]['status'], 'DRAFT')
        self.assertEqual(reports[0]['content'], '제품 소개 미팅')

    def test_create_sequential_id(self):
        """순차 등록 시 ID가 R001, R002, ... 순서로 생성된다."""
        reports, _ = create_report(self.reports, 'C001', '2026-06-01', 'A')
        reports, _ = create_report(reports, 'C001', '2026-06-02', 'B')
        reports, _ = create_report(reports, 'C001', '2026-06-03', 'C')
        self.assertEqual(reports[0]['report_id'], 'R001')
        self.assertEqual(reports[1]['report_id'], 'R002')
        self.assertEqual(reports[2]['report_id'], 'R003')

    def test_create_invalid_customer(self):
        """존재하지 않는 고객사 ID로 등록 시 오류를 반환한다."""
        reports, err = create_report(self.reports, 'C999', '2026-06-09', '내용')
        self.assertEqual(err, '존재하지 않는 고객사입니다.')
        self.assertEqual(len(reports), 0)

    def test_create_empty_customer_id(self):
        """고객사 ID가 비어있으면 오류를 반환한다."""
        reports, err = create_report(self.reports, '', '2026-06-09', '내용')
        self.assertEqual(err, '고객사 ID를 입력해주세요.')

    def test_create_invalid_date_format(self):
        """날짜 형식이 YYYY-MM-DD가 아니면 오류를 반환한다."""
        reports, err = create_report(self.reports, 'C001', '2026/06/09', '내용')
        self.assertEqual(err, '날짜 형식은 YYYY-MM-DD로 입력해주세요.')

    def test_create_nonexistent_date(self):
        """존재하지 않는 날짜(2월30일)면 오류를 반환한다."""
        reports, err = create_report(self.reports, 'C001', '2026-02-30', '내용')
        self.assertEqual(err, '존재하지 않는 날짜입니다.')

    def test_create_invalid_month(self):
        """13월 같이 잘못된 월이면 오류를 반환한다."""
        reports, err = create_report(self.reports, 'C001', '2026-13-01', '내용')
        self.assertEqual(err, '존재하지 않는 날짜입니다.')

    def test_create_empty_date(self):
        """활동일자가 비어있으면 오류를 반환한다."""
        reports, err = create_report(self.reports, 'C001', '', '내용')
        self.assertEqual(err, '활동일자를 입력해주세요.')

    def test_create_empty_content(self):
        """활동 내용이 비어있으면 오류를 반환한다."""
        reports, err = create_report(self.reports, 'C001', '2026-06-09', '')
        self.assertEqual(err, '활동 내용을 입력해주세요.')


class TestReportListAndGet(unittest.TestCase):

    def setUp(self):
        save_data('data/customers.json', [
            {'customer_id': 'C001', 'customer_name': '테스트사', 'manager_name': '홍길동', 'email': 'hong@test.com'}
        ])
        self.reports = []
        self.reports, _ = create_report(self.reports, 'C001', '2026-06-09', 'A')
        self.reports, _ = create_report(self.reports, 'C001', '2026-06-10', 'B')

    def tearDown(self):
        save_data('data/customers.json', [])
        save_data('data/sales_reports.json', [])

    def test_list(self):
        """list_reports는 전체 목록을 반환한다."""
        result = list_reports(self.reports)
        self.assertEqual(len(result), 2)

    def test_get_existing(self):
        """존재하는 ID로 조회하면 해당 영업일지를 반환한다."""
        r = get_report(self.reports, 'R001')
        self.assertIsNotNone(r)
        self.assertEqual(r['content'], 'A')

    def test_get_not_existing(self):
        """존재하지 않는 ID로 조회하면 None을 반환한다."""
        r = get_report(self.reports, 'R999')
        self.assertIsNone(r)


class TestReportUpdate(unittest.TestCase):

    def setUp(self):
        save_data('data/customers.json', [
            {'customer_id': 'C001', 'customer_name': '테스트사', 'manager_name': '홍길동', 'email': 'hong@test.com'}
        ])
        self.reports = []
        self.reports, _ = create_report(self.reports, 'C001', '2026-06-09', '원본내용')

    def tearDown(self):
        save_data('data/customers.json', [])
        save_data('data/sales_reports.json', [])

    def test_update_draft(self):
        """DRAFT 상태에서는 수정이 가능하다."""
        reports, err = update_report(self.reports, 'R001', '2026-06-15', '수정된내용')
        self.assertIsNone(err)
        r = get_report(reports, 'R001')
        self.assertEqual(r['activity_date'], '2026-06-15')
        self.assertEqual(r['content'], '수정된내용')

    def test_update_not_existing(self):
        """존재하지 않는 ID 수정 시 오류를 반환한다."""
        reports, err = update_report(self.reports, 'R999', '2026-06-15', '내용')
        self.assertEqual(err, '존재하지 않는 영업일지입니다.')

    def test_update_non_draft(self):
        """DRAFT가 아닌 상태에서는 수정이 불가능하다."""
        reports, _ = submit_report(self.reports, 'R001')
        reports, err = update_report(reports, 'R001', '2026-06-15', '수정시도')
        self.assertEqual(err, 'DRAFT 상태에서만 수정할 수 있습니다.')


class TestReportStatusTransition(unittest.TestCase):

    def setUp(self):
        save_data('data/customers.json', [
            {'customer_id': 'C001', 'customer_name': '테스트사', 'manager_name': '홍길동', 'email': 'hong@test.com'}
        ])
        self.reports = []
        self.reports, _ = create_report(self.reports, 'C001', '2026-06-09', 'A')

    def tearDown(self):
        save_data('data/customers.json', [])
        save_data('data/sales_reports.json', [])

    def test_submit(self):
        """DRAFT → SUBMITTED 전이가 성공한다."""
        reports, err = submit_report(self.reports, 'R001')
        self.assertIsNone(err)
        self.assertEqual(get_report(reports, 'R001')['status'], 'SUBMITTED')

    def test_approve(self):
        """SUBMITTED → APPROVED 전이가 성공한다."""
        reports, _ = submit_report(self.reports, 'R001')
        reports, err = approve_report(reports, 'R001')
        self.assertIsNone(err)
        self.assertEqual(get_report(reports, 'R001')['status'], 'APPROVED')

    def test_reject(self):
        """SUBMITTED → REJECTED 전이가 성공한다."""
        reports, _ = submit_report(self.reports, 'R001')
        reports, err = reject_report(reports, 'R001')
        self.assertIsNone(err)
        self.assertEqual(get_report(reports, 'R001')['status'], 'REJECTED')

    def test_withdraw(self):
        """SUBMITTED → DRAFT(회수) 전이가 성공한다."""
        reports, _ = submit_report(self.reports, 'R001')
        reports, err = withdraw_report(reports, 'R001')
        self.assertIsNone(err)
        self.assertEqual(get_report(reports, 'R001')['status'], 'DRAFT')

    def test_withdraw_and_resubmit(self):
        """회수 후 다시 상신이 가능하다."""
        reports, _ = submit_report(self.reports, 'R001')
        reports, _ = withdraw_report(reports, 'R001')
        reports, err = submit_report(reports, 'R001')
        self.assertIsNone(err)
        self.assertEqual(get_report(reports, 'R001')['status'], 'SUBMITTED')

    def test_submit_not_draft(self):
        """APPROVED 상태에서 submit 시도 시 차단된다."""
        reports, _ = submit_report(self.reports, 'R001')
        reports, _ = approve_report(reports, 'R001')
        reports, err = submit_report(reports, 'R001')
        self.assertEqual(err, 'DRAFT 상태에서만 상신할 수 있습니다.')

    def test_approve_not_submitted(self):
        """DRAFT 상태에서 approve 시도 시 차단된다."""
        reports, err = approve_report(self.reports, 'R001')
        self.assertEqual(err, 'SUBMITTED 상태에서만 승인할 수 있습니다.')

    def test_reject_not_submitted(self):
        """DRAFT 상태에서 reject 시도 시 차단된다."""
        reports, err = reject_report(self.reports, 'R001')
        self.assertEqual(err, 'SUBMITTED 상태에서만 반려할 수 있습니다.')

    def test_withdraw_not_submitted(self):
        """DRAFT 상태에서 withdraw 시도 시 차단된다."""
        reports, err = withdraw_report(self.reports, 'R001')
        self.assertEqual(err, 'SUBMITTED 상태에서만 회수할 수 있습니다.')

    def test_transition_not_existing(self):
        """존재하지 않는 ID로 상태 전이 시 오류를 반환한다."""
        reports, err = submit_report(self.reports, 'R999')
        self.assertEqual(err, '존재하지 않는 영업일지입니다.')

    def test_full_flow(self):
        """전체 흐름: DRAFT → SUBMIT → APPROVE (정상)"""
        self.assertEqual(get_report(self.reports, 'R001')['status'], 'DRAFT')
        reports, _ = submit_report(self.reports, 'R001')
        self.assertEqual(get_report(reports, 'R001')['status'], 'SUBMITTED')
        reports, _ = approve_report(reports, 'R001')
        self.assertEqual(get_report(reports, 'R001')['status'], 'APPROVED')


if __name__ == '__main__':
    unittest.main()