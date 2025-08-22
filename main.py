from logic.feedback import crear_csv_vacio_si_no_existe
from interface import create_interface

if __name__ == "__main__":
    crear_csv_vacio_si_no_existe()
    app = create_interface()
    app.launch(server_name="0.0.0.0", server_port=8080, share=True)