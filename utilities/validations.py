import re


class RequestHandler():    

    def request_has_JSON(self, request):
        try:
            request.json
            return True
        except:
            return False
    

class ValidateInputs():

    def name_is_valid(self, name=None, min_len=2, max_len=100):
        if name is None or name is "":
            return False, "Name cannot be empty"
        if not isinstance(name, str):
            return False, "Name must be a String"
        if not isinstance(min_len, int):
            min_len = 2
        if not isinstance(max_len, int):
            max_len = 100
        # Check if String contains alphabetical characters
        has_letters = re.search('[a-zA-Z]', name)
        if has_letters is None:
            return False, "Name must contain at least one alphabetical letter"
        # Name starts with a letter
        first_char_is_letter = re.search('[a-zA-Z]', name[:1])
        if first_char_is_letter is None:
            return False, "The first character of the name must be a letter"
        # Ends with letter or number
        last_char_is_letter = re.search('[a-zA-Z]', name[-1:])
        if last_char_is_letter is None:
            return False, "The last character of the name must be a letter or number"
        # check if string contains only allowed characters
        # Allowed are All aphanumeric Underscore (_), dash (-), Space ()
        # The rest must be rejected
        for char in name:
            if re.search('[a-zA-Z0-9]', char) is None:
                if char is not "_" and char is not "-" and char is not " ":
                    return False, "Name can only contain alphanumeric and underscore (_), dash(-) or space( )"
                    
        # test length
        if min_len is not None and min_len > len(name):
            return False, "Name should be at least " + str(min_len) + " characters long"
        if min_len is not None and max_len < len(name):
            return False, "Name should be at most " + str(max_len) + " characters long"
        return True, "OK"
    
    def is_valid_entry_tittle(self, tittle):
        if tittle is None or tittle is "":
            return False, "tittle cannot be empty"
        if not isinstance(tittle, str):
            return False, "tittle must be a String"
        has_letters = re.search('[a-zA-Z]', tittle)
        if has_letters is None:
            return False, "tittle must contain at least one alphabetical letter"
        first_char_is_letter = re.search('[a-zA-Z0-9]', tittle[:1])
        if first_char_is_letter is None:
            return False, "The first character of the tittle must be a letter or a number"
        return True, "OK"
    
    def is_valid_author_name(self, author_name):
        return (self.is_valid_entry_tittle(author_name)[0], 
                    self.is_valid_entry_tittle(author_name)[1].replace("tittle", "Name of the author"))
        
    def is_valid_entry_isbn(self, isbn):
        if isbn is None or isbn is "":
            return False, "ISBN cannot be empty"
        print(type(isbn))
        if type(isbn) != str and type(isbn) != int:
            return False, "ISBN can only be an Integer or a String"
        if not isinstance(isbn, str):
            isbn = str(isbn)
        if isbn.isdigit() == False:
            return False, "ISBN can only contain numbers"
        return True, "OK"
    
                
