from app.UserRepository.user_repositores import UserRepository
class AuthService:
    def __init___(self):
        self.User_Repository= UserRepository()

        def register_user(self, nome:  str, email: str, confirma_senha: str):
            if not nome or not email or not senha:
                raise ValueError("todos os campos são obrigatorios.")

                if senha != confirma_senha:
                    raise ValueError("as senhas não coincidem.")

                    if len(senha)  < 6:
                        raise ValueError("A senha deve ter pelo menos 6 caracteres.")

                        try:
                            uid = self.user_repo.create_user_auth(email, senha, nome)

                            self.user_repo.save_user_data(uid, nome, email)

                            return True, "conta criada com sucesso! faça login para continuar."
                            expect Exception as e:
                            raise Exception(f"erro ao criar conta: {str(e)}")