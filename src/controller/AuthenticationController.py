import jwt
from http import HTTPStatus
from datetime import datetime, timedelta

from persistent.AccountPersistent import AccountPersistent
from models.dto.input.Account import Account as LoginAccount, ResetPassword
from models.dto.input.Account import RegisterAccount
from models.data.Account import Account
from controller.model.ResponseModel import ResponseModel
from config import CONF
from passlib.context import CryptContext

config = CONF["Auth"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthenticationController:
    def __init__(self, session) -> None:
        self.persistent = AccountPersistent(session)

    def login(self, account: LoginAccount) -> ResponseModel:
        user: Account = self.persistent.get_account_by_username(account.username)
        if not user:
            return ResponseModel(
                detail=f"User not found with username {account.username}",
            ).model_dump(), HTTPStatus.NOT_FOUND
        
        if not user.enable:
            return ResponseModel(
                detail=f"User disabled",
            ).model_dump(), HTTPStatus.UNAUTHORIZED

        if not self.__verify_password(account.password, user.password):
            return ResponseModel(
                detail="Invalid credentials",
            ).model_dump(), HTTPStatus.UNAUTHORIZED

        access_token = self.__create_access_token(
            data={"sub": user.username}, expires_delta=timedelta(seconds=config.getint("access_token_expire_time"))
        )
        return ResponseModel(
            data={"access_token": access_token},
            detail="Thành công",
        ).model_dump(), HTTPStatus.OK
    
    def reset_password(self, user, reset_password: ResetPassword):
        user_db = self.persistent.get_account_by_username(user.username)
        if not self.__verify_password(reset_password.old_password, user_db.password):
            return ResponseModel(
                detail="Invalid credentials",
            ).model_dump(), HTTPStatus.UNAUTHORIZED
        user_db.password = pwd_context.hash(reset_password.new_password)
        self.persistent.commit_change()
        return self.login(account=LoginAccount(
            username=user.username,
            password=reset_password.new_password,
        ))
    
    def login_admin(self, account: LoginAccount) -> ResponseModel:
        user: Account = self.persistent.get_account_by_username(account.username)
        if not user:
            return ResponseModel(
                detail=f"User not found with username {account.username}",
            ).model_dump(), HTTPStatus.NOT_FOUND

        if not self.__verify_password(account.password, user.password):
            return ResponseModel(
                detail="Invalid credentials",
            ).model_dump(), HTTPStatus.UNAUTHORIZED
        
        if not user.is_admin:
            return ResponseModel(
                detail="FORBIDDEN",
            ).model_dump(), HTTPStatus.UNAUTHORIZED

        access_token = self.__create_access_token(
            data={"sub": user.username}, expires_delta=timedelta(seconds=config.getint("access_token_expire_time"))
        )
        return ResponseModel(
            data={"access_token": access_token},
            detail="Thành công",
        ).model_dump(), HTTPStatus.OK
    
    def register(self, account: RegisterAccount):
        if self.persistent.is_username_or_email_exist(account.username, account.email):
            return ResponseModel(
                detail="Email or Username already taken",
            ).model_dump(), HTTPStatus.BAD_REQUEST
        
        account_db = self.persistent.create_account(
            username=account.username,
            password=pwd_context.hash(account.password),
            email=account.email,
            fname=account.fname,
            lname=account.lname,
        )
        access_token = self.__create_access_token(
            data={"sub": account_db.username}, expires_delta=timedelta(seconds=config.getint("access_token_expire_time"))
        )
        return ResponseModel(
            data={"access_token": access_token},
            detail="Thành công",
        ).model_dump(), HTTPStatus.OK
    
    def __create_access_token(self, data: dict, expires_delta: timedelta):
        to_encode = data.copy()
        expire = datetime.now() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, config.get("secret_key"), algorithm=config.get("algorithm"))
        return encoded_jwt
    
    def __verify_password(self, plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)