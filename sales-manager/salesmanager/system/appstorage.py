import os
import json
import platform
from pathlib import Path
from configparser import ConfigParser
from hashlib import blake2b
from typing import Final

# Prepare the environment
APP_FOLDER: Path = None
K_SALES = "k-sales"

if platform.system() == "Windows":
    localappdata = Path(os.environ["LOCALAPPDATA"])
    for dir_ in localappdata.iterdir():
        if dir_.name == K_SALES:
            APP_FOLDER = dir_
            break

    if APP_FOLDER is None:
        ap = localappdata/K_SALES
        ap.mkdir()
        APP_FOLDER = ap
else:
    raise OSError("unsupported operating system")


class BaseAccount:

    def __init__(self, acc_file: Path):
        self.acc_file = acc_file


class AdminAccount(BaseAccount):

    def __init__(self, acc_file: Path):
        super(AdminAccount, self).__init__(acc_file)


class EmployeeAccount(BaseAccount):

    def __init__(self, acc_file: Path):
        super(EmployeeAccount, self).__init__(acc_file)


class AccountManager:

    __slots__ = ("_account_dir", "_accounts", "_admin_account", "_setup")

    def __init__(self, Acc_dir):
        self._account_dir: Path = Acc_dir
        self._setup = False
        self._admin_account: dict[tuple[str, str], Path] = {}
        self._accounts: dict[tuple[str, str], Path] = self._load_accounts()

    @property
    def account_dir(self):
        return self._account_dir

    @property
    def accounts(self):
        return self._accounts

    @property
    def admin_account(self):
        return self._admin_account

    @property
    def setup(self):
        return self._setup

    def create(self, user_name: str, password: str, *, admin=False) -> BaseAccount:
        """ Use the user_name and password to create an account file.
            The username and password are hashed using blake2b. The result is
            combined and separated by a hyphen.
        """

        user_name_enc = blake2b(user_name.encode(), digest_size=10).hexdigest()
        password_enc = blake2b(password.encode(), digest_size=10).hexdigest()
        if ((login_dets := (user_name_enc, password_enc)) in self._accounts or login_dets in self._admin_account):
            return None
        acc_name = "-".join([user_name_enc, password_enc]
                            ) if admin is False else "-".join(["ADMIN", user_name_enc, password_enc])
        new_acc_file = self.account_dir/acc_name
        os.open(str(new_acc_file), os.O_CREAT)
        if admin:
            if self._setup:
                raise AdminExists("admin account already exists")
            self._setup = True
            self._admin_account[(user_name_enc, password_enc)] = new_acc_file
            return AdminAccount(new_acc_file)
        self._accounts[(user_name_enc, password_enc)] = new_acc_file
        return Account(new_acc_file)

    def load(self, user_name: str, password: bytes, *, admin=False) -> BaseAccount:
        """
        load account from self.accounts or load the admin account. Hashes the user_name
        and password and compares if the hash exists in the accounts dictionary
        """
        user_name_enc = blake2b(user_name.encode(), digest_size=10).hexdigest()
        password_enc = blake2b(password.encode(), digest_size=10).hexdigest()
        if admin:
            admin_acc = self._admin_account[(user_name_enc, password_enc)] if (
                user_name_enc, password_enc) in self._admin_account else None
            return admin_acc
        for login_dets in self._accounts:
            enc_user, enc_pass = login_dets
            if (user_name_enc == enc_user and password_enc == enc_pass):
                return Account(self.accounts[login_dets])
        return None

    def _load_accounts(self):
        """
        Load all accounts in the account directory into self.accounts
        """
        accounts = {}

        def acc_build(acc_path: Path):
            acc_name = acc_path.stem
            try:
                user_name, pass_word = acc_name.split("-")
            except ValueError:
                if acc_name.startswith("ADMIN"):
                    admin_name, admin_pass = acc_name.lstrip(
                        "ADMIN-").split("-")
                    self._admin_account[(admin_name, admin_pass)] = acc_path
                    self._setup = True
            else:
                return user_name, pass_word

        for acc_path in self.account_dir.iterdir():
            acc_key = acc_build(acc_path)
            if acc_key:
                accounts[acc_key] = acc_path
        return accounts


class AdminExists(Exception):
    pass
