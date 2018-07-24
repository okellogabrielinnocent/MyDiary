import re

   

class ValidateInputs():

        

    @classmethod
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
    
    @classmethod
    def is_valid_author_name(self, author_name):
        return (self.is_valid_entry_tittle(author_name)[0], 
                    self.is_valid_entry_tittle(author_name)[1].replace("tittle", "Name of the author"))

    @classmethod    
    def is_valid_entry_body(self, body):
        if body is None or body is "":
            return False, "Body cannot be empty"
        print(type(body))
        if type(body) != str and type(body) != int:
            return False, "Body can only be an Integer or a String"
        if not isinstance(body, str):
            body = str(body)
        if body.isdigit() == False:
            return False, "body can only contain numbers"
        return True, "OK"
    
                
