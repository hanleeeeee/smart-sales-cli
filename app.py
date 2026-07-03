from src.menu import customer_menu, report_menu, summary_menu, export_csv_menu


def main():
    while True:
        print('\n' + '=' * 50)
        print('Smart Sales CLI')
        print('=' * 50)
        print('1. 고객사 관리')
        print('2. 영업일지 관리')
        print('3. 고객사별 활동 요약')
        print('4. CSV 내보내기')
        print('5. 종료')
        print('=' * 50)

        choice = input('선택: ').strip()

        if choice == '1':
            customer_menu()
        elif choice == '2':
            report_menu()
        elif choice == '3':
            summary_menu()
        elif choice == '4':
            export_csv_menu()
        elif choice == '5':
            print('프로그램을 종료합니다.')
            break
        else:
            print('잘못된 선택입니다. 다시 입력해주세요.')


if __name__ == '__main__':
    main()
