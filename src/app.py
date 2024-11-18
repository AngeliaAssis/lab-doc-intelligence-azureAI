import streamlit as st
from services.blob_service import upload_blob
from services.credit_card_service import analyze_credit_card
def configure_interface():
    st.title("Upload de Arquivos DIO - Desafio - AZURE_FAKE DOCS")
    uploaded_file = st.file.uploader("Escolha um arquivo", type=["png", "jpg", "jpeg", "pdf"])

    if uploaded_file is not None:
        filename = uploaded_file.name
        # enviar para o blob storage
        blob_url = upload_blob(uploaded_file, filename)
        if blob_url:
            st.write(f"Arquivo {filename} enviado com sucesso para o Azure Blob Storage")
            # chamar função de detecção de informações de cartão de crédito
            credit_card_info = analyze_credit_card(blob_url)
            show_image_and_validation(blob_url, credit_card_info)
        else:
            st.write(f"Erro ao enviar o arquivo {filename} para o Azure Blob Storage")

def show_image_and_validation(blob_url, credit_card_info):
    st.image(blob_url, caption="Imagem enviada", use_column_width=True)
    st.write("Resultado da validação:")
    if credit_card_info and credit_card_info["card_name"]:
        st.markdown(f"<h1 style='color: green;'>Cartão Válido</h1>", unsafe_allow_html=True)
        st.write(f"Nome do Titular: {credit_card_info['card_name']}")
        st.write(f"Data de validade: {credit_card_info['expiry_date']}")
    else:
        st.markdown(f"<h1 style='color: red;'>Cartão Inválido</h1>", unsafe_allow_html=True)
        st.write("Este não é um cartão de crédito válido")


if __name__ == "__main__":
    configure_interface()
