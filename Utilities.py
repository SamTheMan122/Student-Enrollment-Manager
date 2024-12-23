from pprint import pformat

from pymongo.errors import OperationFailure
from mongoengine import *
import io


class Utilities:
    """startup - creates the connection and returns the database client."""

    @staticmethod
    def startup():
        # print("Prompting for the password.")
        while True:
            # password = getpass.getpass(prompt='MongoDB password --> ')
            #cluster = f"mongodb+srv://CECS-323-Spring-2024-User:{password}@cluster0.uhlmij5.mongodb.net/?retryWrites=true&w=majority"
            cluster = "mongodb+srv://sam19r2:password1234@entry1.fyjpm.mongodb.net/?retryWrites=true&w=majority&appName=Entry1"
            database_name = "Entry1"
            client = connect(db=database_name, host=cluster)
            try:
                junk = client.server_info()  # Test the connection
                return client
            except OperationFailure as OE:
                print(OE)
                print("Error, invalid password.  Try again.")

    @staticmethod
    def print_exception(thrown_exception: Exception):
        """
        :param thrown_exception:    The exception that MongoDB threw.
        :return:                    The formatted text describing the issue(s) in the exception.
        """
        # Use StringIO as a buffer to accumulate the output.
        with io.StringIO() as output:
            output.write('***************** Start of Exception print *****************\n')
            output.write(f'The exception is of type: {type(thrown_exception).__name__}\n')
            # DuplicateKeyError is a subtype of WriteError.  So I have to check for DuplicateKeyError first, and then
            # NOT check for WriteError to get this to work properly.
            if isinstance(thrown_exception, NotUniqueError):
                error = thrown_exception.args[0]  # get the full text of the error message.
                message = error[error.index('index:') + 7:error.index('}')]  # trim off the unwanted parts
                index_name = message[:message.index(' ')]
                field_list = message[message.index('{') + 2:]  # Extract a string dictionary of the index fields.
                fields = []  # The list of fields in the violated uniqueness constraint.
                while field_list.find(':') > 0:  # Keep going until we've gotten all of the fields.
                    field_length = field_list.find(':')
                    field = field_list[:field_length]
                    fields.append(field)
                    # Trim off the latest field and get ready to get the next field name.
                    if (field_list.find(', ')) > 0:  # at least one more field to report.
                        field_list = field_list[field_list.find(', ') + 2:]
                    else:  # signal that we're done.
                        field_list = ''
                output.write(f'Uniqueness constraint violated: {index_name} with fields:\n{fields}')
            elif isinstance(thrown_exception, ValidationError):
                output.write(f'{pformat(thrown_exception.message)}\n')
                errors = thrown_exception.errors
                for error in errors.keys():
                    output.write(f'field name: {error} has issue: \n{pformat(errors.get(error))}\n')
            results = output.getvalue().rstrip()
        return results
