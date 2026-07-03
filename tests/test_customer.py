import unittest
import os
import csv
import shutil
from src.customer import (
    create_customer, list_customers, get_customer,
    search_customers, update_customer, delete_customer,
    export_customers_to_csv
)
from src.storage import save_data, load_data


class TestCustomerCreate(unittest.TestCase):

    def setUp(self):
        self.customers = []

    def test_create_normal(self):
        """정상 등록 시 customer_id가 C001부터 생성된다."""
        customers, err = create_customer(self.customers, '테스트사', '홍길동', 'hong@test.com')
        self.assertIsNone(err)
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0]['customer_id'], 'C001')
        self.assertEqual(customers[0]['customer_name'], '테스트사')
        self.assertEqual(customers[0]['manager_name'], '홍길동')
        self.assertEqual(customers[0]['email'], 'hong@test.com')

    def test_create_sequential_id(self):
        """순차 등록 시 ID가 C001, C002, ... 순서로 생성된다."""
        customers, _ = create_customer(self.customers, 'A', 'M1', 'a@test.com')
        customers, _ = create_customer(customers, 'B', 'M2', 'b@test.com')
        customers, _ = create_customer(customers, 'C', 'M3', 'c@test.com')
        self.assertEqual(customers[0]['customer_id'], 'C001')
        self.assertEqual(customers[1]['customer_id'], 'C002')
        self.assertEqual(customers[2]['customer_id'], 'C003')

    def test_create_empty_name(self):
        """고객사명이 빈 문자열이면 오류를 반환한다."""
        customers, err = create_customer(self.customers, '', '홍길동', 'hong@test.com')
        self.assertEqual(err, '고객사명을 입력해주세요.')
        self.assertEqual(len(customers), 0)

    def test_create_blank_name(self):
        """고객사명이 공백만 있으면 오류를 반환한다."""
        customers, err = create_customer(self.customers, '   ', '홍길동', 'hong@test.com')
        self.assertEqual(err, '고객사명을 입력해주세요.')
        self.assertEqual(len(customers), 0)

    def test_create_empty_manager(self):
        """담당자명이 빈 문자열이면 오류를 반환한다."""
        customers, err = create_customer(self.customers, '테스트사', '', 'hong@test.com')
        self.assertEqual(err, '담당자명을 입력해주세요.')
        self.assertEqual(len(customers), 0)

    def test_create_empty_email(self):
        """이메일이 빈 문자열이면 오류를 반환한다."""
        customers, err = create_customer(self.customers, '테스트사', '홍길동', '')
        self.assertEqual(err, '이메일을 입력해주세요.')
        self.assertEqual(len(customers), 0)

    def test_create_invalid_email(self):
        """이메일에 @가 없으면 오류를 반환한다."""
        customers, err = create_customer(self.customers, '테스트사', '홍길동', 'invalid')
        self.assertEqual(err, '올바른 이메일 형식이 아닙니다.')
        self.assertEqual(len(customers), 0)

    def test_create_duplicate_email(self):
        """동일한 이메일로 등록하면 오류를 반환한다."""
        customers, _ = create_customer(self.customers, 'A', 'M1', 'dup@test.com')
        customers, err = create_customer(customers, 'B', 'M2', 'dup@test.com')
        self.assertEqual(err, '이미 등록된 이메일입니다.')
        self.assertEqual(len(customers), 1)


class TestCustomerListAndGet(unittest.TestCase):

    def setUp(self):
        self.customers = []
        self.customers, _ = create_customer(self.customers, 'A', 'M1', 'a@test.com')
        self.customers, _ = create_customer(self.customers, 'B', 'M2', 'b@test.com')

    def test_list(self):
        """list_customers는 전체 목록을 반환한다."""
        result = list_customers(self.customers)
        self.assertEqual(len(result), 2)

    def test_list_copy(self):
        """list_customers는 원본과 다른 리스트를 반환한다."""
        result = list_customers(self.customers)
        result.append({'dummy': True})
        self.assertEqual(len(self.customers), 2)

    def test_get_existing(self):
        """존재하는 ID로 조회하면 해당 고객사를 반환한다."""
        c = get_customer(self.customers, 'C001')
        self.assertIsNotNone(c)
        self.assertEqual(c['customer_name'], 'A')

    def test_get_not_existing(self):
        """존재하지 않는 ID로 조회하면 None을 반환한다."""
        c = get_customer(self.customers, 'C999')
        self.assertIsNone(c)


class TestCustomerSearch(unittest.TestCase):

    def setUp(self):
        self.customers = []
        self.customers, _ = create_customer(self.customers, '삼성전자', '홍길동', 'hong@test.com')
        self.customers, _ = create_customer(self.customers, 'LG전자', '김철수', 'kim@test.com')
        self.customers, _ = create_customer(self.customers, '네이버', '이몽룡', 'lee@test.com')

    def test_search_by_name(self):
        """고객사명으로 부분 일치 검색된다."""
        result = search_customers(self.customers, '전자')
        self.assertEqual(len(result), 2)

    def test_search_by_manager(self):
        """담당자명으로 부분 일치 검색된다."""
        result = search_customers(self.customers, '김철')
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['customer_id'], 'C002')

    def test_search_no_result(self):
        """일치하는 항목이 없으면 빈 리스트를 반환한다."""
        result = search_customers(self.customers, '없음')
        self.assertEqual(len(result), 0)

    def test_search_empty_keyword(self):
        """검색어가 비어있으면 전체 목록을 반환한다."""
        result = search_customers(self.customers, '')
        self.assertEqual(len(result), 3)

    def test_search_case_insensitive(self):
        """대소문자를 구분하지 않고 검색된다."""
        result = search_customers(self.customers, '삼성')
        self.assertEqual(len(result), 1)


class TestCustomerUpdate(unittest.TestCase):

    def setUp(self):
        self.customers = []
        self.customers, _ = create_customer(self.customers, '원본', '홍길동', 'hong@test.com')
        self.customers, _ = create_customer(self.customers, '중복검증용', '김철수', 'kim@test.com')

    def test_update_normal(self):
        """정상 수정 시 정보가 변경된다."""
        customers, err = update_customer(self.customers, 'C001', '수정된이름', '이몽룡', 'lee@test.com')
        self.assertIsNone(err)
        c = get_customer(customers, 'C001')
        self.assertEqual(c['customer_name'], '수정된이름')
        self.assertEqual(c['manager_name'], '이몽룡')
        self.assertEqual(c['email'], 'lee@test.com')

    def test_update_not_existing(self):
        """존재하지 않는 ID 수정 시 오류를 반환한다."""
        customers, err = update_customer(self.customers, 'C999', 'X', 'Y', 'z@test.com')
        self.assertEqual(err, '존재하지 않는 고객사입니다.')

    def test_update_duplicate_email(self):
        """수정 시 다른 고객사가 사용 중인 이메일로 변경하면 오류를 반환한다."""
        customers, err = update_customer(self.customers, 'C001', '변경', '담당자', 'kim@test.com')
        self.assertEqual(err, '이미 등록된 이메일입니다.')

    def test_update_self_email_allowed(self):
        """자기 자신의 이메일로는 수정이 허용된다."""
        customers, err = update_customer(self.customers, 'C001', '변경', '담당자', 'hong@test.com')
        self.assertIsNone(err)


class TestCustomerDelete(unittest.TestCase):

    def setUp(self):
        self.customers = []
        self.customers, _ = create_customer(self.customers, '삭제할고객', '홍길동', 'hong@test.com')

    def tearDown(self):
        # 테스트 후 데이터 파일 정리
        save_data('data/sales_reports.json', [])

    def test_delete_normal(self):
        """영업일지가 없는 고객사는 삭제 가능하다."""
        save_data('data/sales_reports.json', [])
        customers, err = delete_customer(self.customers, 'C001')
        self.assertIsNone(err)
        self.assertEqual(len(customers), 0)

    def test_delete_with_reports(self):
        """영업일지가 있는 고객사는 삭제 불가."""
        save_data('data/sales_reports.json', [
            {'report_id': 'R001', 'customer_id': 'C001', 'status': 'DRAFT'}
        ])
        customers, err = delete_customer(self.customers, 'C001')
        self.assertEqual(err, '해당 고객사의 영업일지가 존재하여 삭제할 수 없습니다.')
        self.assertEqual(len(customers), 1)

    def test_delete_not_existing(self):
        """존재하지 않는 ID 삭제 시 오류를 반환한다."""
        customers, err = delete_customer(self.customers, 'C999')
        self.assertEqual(err, '존재하지 않는 고객사입니다.')


class TestCustomerExportCsv(unittest.TestCase):

    def setUp(self):
        self.customers = []
        self.customers, _ = create_customer(self.customers, 'A', 'M1', 'a@test.com')
        self.customers, _ = create_customer(self.customers, 'B', 'M2', 'b@test.com')

    def test_export_normal(self):
        """정상 CSV 내보내기 시 파일이 생성되고 내용이 일치한다."""
        filepath, err = export_customers_to_csv(self.customers, 'exports')
        self.assertIsNone(err)
        self.assertIsNotNone(filepath)
        self.assertTrue(os.path.exists(filepath))

        with open(filepath, 'r', encoding='utf-8-sig', newline='') as f:
            reader = list(csv.reader(f))
        self.assertEqual(reader[0], ['customer_id', 'customer_name', 'manager_name', 'email'])
        self.assertEqual(len(reader), 3)
        self.assertEqual(reader[1][0], 'C001')

    def test_export_empty(self):
        """고객사가 없으면 빈 헤더만 있는 CSV가 생성된다."""
        filepath, err = export_customers_to_csv([], 'exports')
        self.assertIsNone(err)
        with open(filepath, 'r', encoding='utf-8-sig', newline='') as f:
            reader = list(csv.reader(f))
        self.assertEqual(len(reader), 1)


if __name__ == '__main__':
    unittest.main()