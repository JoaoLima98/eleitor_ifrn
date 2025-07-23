'''import psycopg2


class PessoaRepository:

    def __init__(self):
        self.conn = psycopg2.connect(dbname="eleicao", user="postgres", password="87654321", host="localhost", port="5432")


    def get_cpf_pessoas(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT cpf FROM pessoas")
            return [row[0] for row in cur.fetchall()]
        
    def get_email_pessoas(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT email FROM pessoas")
            return [row[0] for row in cur.fetchall()]'''
            
            
            

class PessoaRepository:
    
    def get_cpf_unico(self, cpf: str):
        lista_de_cpf = [
            "11568675411",
            "12345678910"
        ]
        if cpf in lista_de_cpf:
            return None
        return cpf
        
    def get_email_unico(self, email: str):
        lista_de_emails = [
            "joaode@gmail.com",
            "jesus@gmail.com"
        ]
        if email in lista_de_emails:
            return None
        return email
        
