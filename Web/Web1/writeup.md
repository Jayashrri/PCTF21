# Blind Assisstant

The given chall uses blind boolean injection. But not all the input fields are unsanitized for injection. Only the search field on the index page is vulnerable to injection. This can be tested by using blind boolean injection technique. We know by supplying various inputs that the patter of the seach parameter is pattern matched. So the query should be something like `SELCT * FROM products WHERE productname LIKE %$search%`.
Using blind boolean injection `p' AND 1=1 -- ` and `p' AND 1=2 --` we find this is the field vulnerable to injection. Now we know flag is hidden in code. Trying to input `p' or 1=1 -- ` does not work successfully as they are deliberately preventing flag from printing.

The table name and the number of parmeters can be found by brute forcing as the server returns injection failed response.
Finally, we find that the payload `i' UNION SELECT NULL, NULL, (SELECT GROUP_CONCAT(code) from products ) -- ` reveals the necessary flag `p_ctf{41w4y5_54n1t1z3_1nput}` .
