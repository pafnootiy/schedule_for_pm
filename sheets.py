import os
from string import ascii_uppercase

import gspread
from dotenv import load_dotenv

import config
from utils import parse_json


def get_client(client_secret_filename: str) -> gspread.Client:
    return gspread.service_account(filename=client_secret_filename)


def get_spreadsheet(client: gspread.Client, title: str) -> gspread.Spreadsheet:
    return client.open(title)


def get_worksheet(spreadsheet: gspread.Spreadsheet, title: str) -> gspread.Worksheet:
    return spreadsheet.worksheet(title)


def create_spreadsheet(
    client: gspread.Client, spreadsheet_title: str
) -> gspread.Spreadsheet:
    return client.create(spreadsheet_title)


def create_sheet(
    spreadsheet: gspread.Spreadsheet, sheet_title: str, headers: list, style: dict
):
    sheet: gspread.Worksheet = spreadsheet.add_worksheet(
        title=sheet_title, rows="100", cols="20"
    )
    sheet.insert_row(headers)
    headers_range = f"A1:{ascii_uppercase[len(headers)-1]}1"
    sheet.format(headers_range, style)

    return sheet


def prepare_sheets(client: gspread.Client, spreadsheet_title: str, admin_email: str):
    spreadsheet = create_spreadsheet(client, spreadsheet_title)

    students_sheet = create_sheet(
        spreadsheet=spreadsheet,
        sheet_title=config.STUDENTS_TITLE,
        headers=config.STUDENTS_HEADERS,
        style=config.HEADERS_STYLE,
    )
    pm_sheet = create_sheet(
        spreadsheet=spreadsheet,
        sheet_title=config.PM_TITLE,
        headers=config.PM_HEADERS,
        style=config.HEADERS_STYLE,
    )

    # push parsed from json files data
    student_profiles: list[dict] = parse_json(f"{config.STUDENTS_TITLE}.json")
    pm_profiles: list[dict] = parse_json(f"{config.PM_TITLE}.json")
    push_profiles(students_sheet, student_profiles)
    push_profiles(pm_sheet, pm_profiles)

    # delete default 'Sheet1'
    sheet1 = spreadsheet.sheet1
    spreadsheet.del_worksheet(sheet1)

    # share with admin
    spreadsheet.share(value=admin_email, perm_type="user", role="owner")

    return spreadsheet.url


def push_profiles(worksheet: gspread.Worksheet, profiles: list[dict]) -> None:
    rows = [list(profile.values()) for profile in profiles]
    return worksheet.append_rows(rows)


def get_student_row(worksheet: gspread.worksheet, tg_username: str) -> int:
    cell_row = worksheet.find(tg_username).row
    return cell_row


def main():
    load_dotenv()
    secret = os.getenv("SERVICE_ACCOUNT_JSON")
    client = get_client(secret)

    # prepare_sheets(client, config.SPREADSHEET_TITLE, os.getenv("ADMIN_EMAIL"))

    spreadsheet = get_spreadsheet(client, config.SPREADSHEET_TITLE)

    students_sheet = get_worksheet(spreadsheet, config.STUDENTS_TITLE)
    pm_sheet = get_worksheet(spreadsheet, config.PM_TITLE)

    print(students_sheet.get_all_records())
    print(pm_sheet.get_all_records())


if __name__ == "__main__":
    main()
