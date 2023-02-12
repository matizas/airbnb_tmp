" The entry point of the command interpreter "

import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    " The Command Interface class which inherits the Cmd class "

    prompt = "(hbnb) "
    __class_set = set()
    __all_records = {}

    def emptyline(self):
        pass

    def preloop(self):
        HBNBCommand.__all_records = storage.all()
        __globals = {**globals()}

        for key in __globals:
            value = __globals[key]

            if type(value).__name__ == "type" and issubclass(value, BaseModel):
                HBNBCommand.__class_set.add(key)

    def do_quit(self, line):
        " Exits the Console"
        return True

    def do_EOF(self, line):
        " Exits the Console"
        return True

    @staticmethod
    def get_args_from_line(line):
        if not line:
            return None

        return line.split(" ")

    @classmethod
    def __validate_n_run(cls, command, line):
        '''
        This class static methods validates input from the console
        and execute command if validation is successful
        Parameters
        ----------
        cls : object - class object
        command : function - callback function to be executed
        line : line from the console
        '''
        command_name = command.__name__

        line_args = cls.get_args_from_line(line)
        if not line_args:
            print("** class name missing **")

        elif line_args[0] not in cls.__class_set:
            print("** class doesn't exist **")

        else:
            if command_name == "exec_create":
                command(line_args[0])
            elif len(line_args) <= 2:
                if len(line_args) == 1:
                    print("** instance id missing **")
                elif len(line_args) == 2:
                    [cls_name, id] = line_args
                    cls_name_id_key = cls_name+"."+id

                    if cls_name_id_key not in HBNBCommand.__all_records:
                        print("** no instance found **")
                    else:
                        command(cls_name_id_key)
            elif len(line_args) <= 4:
                if command_name == "exec_update":
                    command(line_args)

    def do_create(self, line):
        '''
        This command creates a new instance of a Model
        Parameter
        ---------
        line : str - Name of Class
        '''
        def exec_create(cls_name):
            " Executes the create command "
            newObj = globals()[cls_name]()
            newObj.save()
            print(newObj.id)

        HBNBCommand.__validate_n_run(exec_create, line)

    def do_show(self, line):
        '''
        This command shows details of an existing instance
        Parameters
        ---------
        line : str - Name of Class and id
        '''
        def exec_show(cls_name_id_key):
            " Executes the show command "
            cls_name = cls_name_id_key.split(".")[0]
            selected_rec_obj = HBNBCommand.__all_records[cls_name_id_key]
            print(selected_rec_obj.__str__())

        HBNBCommand.__validate_n_run(exec_show, line)

    def do_destroy(self, line):
        '''
        This command destroys an existing instance
        Parameters
        ---------
        line : str - Name of Class and id
        '''
        def exec_destroy(cls_name_id_key):
            " Executes the destroy command "
            HBNBCommand.__all_records.pop(cls_name_id_key)
            storage.save()

        HBNBCommand.__validate_n_run(exec_destroy, line)

    def do_all(self, line):
        '''
        Prints all string representation of all instances
        based or not on the class name
        Parameters
        ---------
        line : str - Name of Class (Optional)
        '''
        data_list = []
        all_records = HBNBCommand.__all_records

        if not line:
            for key in all_records:
                data_list.append(all_records[key].__str__())
            print(data_list)
        elif line not in HBNBCommand.__class_set:
            print("** class doesn't exist **")
        else:
            print(globals()[line].all())

    def do_update(self, line):
        " update <class name> <id> <attribute name> '<attribute value>'"

        def exec_update(line_args):
            " Executes the update command "

            if len(line_args) == 2:
                print("** attribute name missing **")
            elif len(line_args) == 3:
                print("** value missing **")
            else:
                [cls_name, id, attr_name, attr_value] = line_args
                all_records = HBNBCommand.__all_records
                cls_name_id_key = cls_name+"."+id
                selected_record = all_records[cls_name_id_key]

                if attr_name not in ["id", "created_at", "updated_at"]:
                    try:
                        value = eval(attr_value)
                        selected_record.__setattr__(attr_name, value)
                        selected_record.save()
                    except Exception as e:
                        print(str(e))

        HBNBCommand.__validate_n_run(exec_update, line)

    @staticmethod
    def default_parser(line):
        pattern = "^(?P<cls_name>[a-zA-Z]+)\.(?P<method_name>[a-zA-Z]+)\((?P<args>.*)\)"

        test = re.match(pattern, line)
        if test:
            sout1 = test.group("cls_name")
            sout2 = test.group("method_name")
            sout3 = test.group("args")
            return [sout1, sout2, sout3]

        return None

    @staticmethod
    def args_update_parser(args_list):
        _list = [None] * 3
        [id, *rest] = args_list
        attr_name = ""
        attr_value = ""
        id = id.strip("'\"")
        _list[0] = id

        if len(rest) == 2:
            [attr_name, attr_value] = rest
            attr_name = attr_name.strip("'\" ")
            attr_value = attr_value.strip(" ")

        elif len(rest) == 1:
            arg2 = rest[0]
            [attr_name, attr_value] = arg2.split(":")
            attr_name = attr_name.strip("{'\" ")
            attr_value = attr_value.strip("} ")

        _list[1] = attr_name
        _list[2] = attr_value
        return _list

    def default(self, line):
        parsed_line = HBNBCommand.default_parser(line)

        if parsed_line:
            [cls_name, method_name, args] = parsed_line
            args_list = args.split(",")

            if cls_name in HBNBCommand.__class_set:
                cls_obj = globals()[cls_name]
                status = ["show", "destroy"] and len(args_list)

                if method_name in ["all", "count"]:
                    print(getattr(cls_obj, method_name)())

                elif method_name in status == 1:
                    id = args.strip('"')
                    called_method = getattr(cls_obj, method_name)(id)

                    if called_method == 1:
                        print("** instance id missing **")
                    elif called_method == 2:
                        print("** no instance found **")
                    else:
                        if method_name == "show":
                            print(called_method)    # show method
                elif method_name == "update":
                    parsed_args = HBNBCommand.args_update_parser(args_list)
                    getattr(cls_obj, method_name)(*parsed_args)
                else:
                    print("*** Unknown syntax: "+line)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
