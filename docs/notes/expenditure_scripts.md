# Expenditure Scripts

I am going to describe the functionality I would like from the expenditure scripts using a technique from Clean Code.

I want to automatically submit daily expenditure.

To automatically submit daily expenditure, I need to parse the expenditure sheet and then post a submission for each row of the sheet parsed.

To parse the expenditure sheet, I need to open the expenditure sheet and store each row in an appropriate format.

To open the expenditure sheet, I need to authenticate using gspread, open the workbook containing the expenditure sheet and then open the worksheet.

authenticate()

open_workbook(), get_workbook()

open_worksheet(), get_worksheet()

To store each row in an appropriate format, I need to read each row and then write that output to a variable.

read_row(), get_row()

write_row(), store_row()

To post a submission for each row of the sheet parsed, I need to build the request and then submit the request.

build_request(row), row.build_request()

submit_request(row), row.submit_request()

### Thoughts.

I should separate parsing and submitting. That way, I can keep an active record of what I've submitted (the parse can be edited but the sheet can't).

I need to decide on what I want my classes to be. I have a bunch of options but I think the key things to bear in mind when deciding are:
* Encapsulation. Keep dependent pieces together and separate everything else. This way, if something breaks or changes (e.g. authentication method changes), only one piece of the code needs to be changed. This has the added benefit that the code can be reused.
* Functionality when recovering from errors. It is crucial that expenditure is only submitted once. As such, there needs to be a way of ensuring that manual runs do not submit (at least easily) entries that have already been submitted that day.
