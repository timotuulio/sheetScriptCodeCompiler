... Create variables of type sheet and add them to symbol table ...
sheet S
sheet SHEETVARII = 5 * 6
sheet SHEETVARIII = {1.0 , 2.0  3.0 , 4.0 5.0 , 6.0}
sheet SHEETVARIV = {1.0+-2.0 3.0+4.0 5.0 - 6.0}

... Create variables of type range and add them to symbol table ...
range _rangevar0 = range SHEETVAR ' AZ1 .. $
range _rangevar1 = range SHEETVAR'A1 .. SHEETVAR'B1
range _rangevar2 = range SHEETVAR'B2 .. SHEETVAR'B3
range _rangevar3 = range SHEETVAR'Z4 .. SHEETVAR'BA4
range _rangevar4 = range SHEETVAR'A8 .. SHEETVAR'B9
range _rangevar5 = range SHEETVAR'A9 .. SHEETVA'B9


... Create variables of type scalar and add them to symbol table ...
scalar forty = 10.0 + 30.0
scalar thirty = 40.0 - 10.0 * 3.0 + 20.0
scalar ten = 5.0 * 2.0 + 40.0 / 4.0 - 5.0 * 2.0
scalar twelve = 24.0 / 2.0
scalar twoOne = forty + ten

... Print number, variable and the result of a calculation ...
print_scalar 1.0
print_scalar ten
print_scalar 1.0 + 56.0 * 2.0 - 12.0
