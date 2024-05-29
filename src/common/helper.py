from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from config import CONF
from persistent.AccountPersistent import AccountPersistent
from persistent.RecruiterPersistent import RecruiterPersistent
from persistent.ApplicantPersistent import ApplicantPersistent
from common.database_connection import get_db
from common.constant import RECRUITER_ROLE, ADMIN_ROLE, APPLICANT_ROLE
from models.dto.output.AccountDTO import Account, ApplicantDTO, RecruiterInfoDTO

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(role = ["*"]):
    def role_checker(token: str = Depends(oauth2_scheme), session = Depends(get_db)):
        auth_config = CONF["Auth"]
        persistent = AccountPersistent(session)
        recruiter_persistent = RecruiterPersistent(session)
        applicant_persistent = ApplicantPersistent(session)
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
        forbidden_exception = HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Resource forbidden",
        )
        try:
            payload = jwt.decode(token, auth_config.get("secret_key"), algorithms=[auth_config.get("algorithm")])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except jwt.ExpiredSignatureError:
            raise credentials_exception
        except jwt.DecodeError:
            raise credentials_exception
        user = persistent.get_account_by_username(username)
        if user is None:
            raise credentials_exception

        applicant = applicant_persistent.get_applicant_by_account_id(user.id)
        recruiter = recruiter_persistent.get_recruiter_by_account_id(user.id)
        user = Account(
            **user.to_dict(),
            applicant=ApplicantDTO(**applicant.to_dict()) if applicant else None,
            recruiter=RecruiterInfoDTO(**recruiter.to_dict()) if recruiter else None
        )
        print(user.model_dump())
        if "*" in role:
            return user
        elif ADMIN_ROLE in role and user.is_admin:
            return user
        else:
            if APPLICANT_ROLE in role and user.applicant:
                return user
            if RECRUITER_ROLE in role and user.recruiter:
                return user

        raise forbidden_exception

    return role_checker
