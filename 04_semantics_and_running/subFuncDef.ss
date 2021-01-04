... Subroutine definition, gives an error "Error, unknown node of type subroutine definition" but that's  to be expected ...
subroutine Subberiroutine
[variable : scalar, _aA4 : range, SHEETVAR : sheet]
is
scalar scalarVar = -2.2*3.3+4.4
print_sheet SHEETSUBBER
end

... Function definition, gives an error "Error, unknown node of type function definition" but that's  to be expected ...
function Functioabc [ _aA4 : range, SHEETVAR : sheet]
return range is
sheet SHEETVAR = 5 * 6
print_sheet SHEETASD
end

print_scalar 1.0