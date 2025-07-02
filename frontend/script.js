document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('investimentoForm');
    const resultadoContainer = document.getElementById('resultado');
    const erroContainer = document.getElementById('erro');
    const irContainer = document.getElementById('irContainer');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Mostrar loading
        const btnCalcular = document.querySelector('.btn-calcular');
        const originalText = btnCalcular.textContent;
        btnCalcular.textContent = 'Calculando...';
        btnCalcular.disabled = true;

        // Esconder resultados anteriores
        resultadoContainer.style.display = 'none';
        erroContainer.style.display = 'none';

        try {
            // Capturar dados do formulário
            const formData = new FormData(form);
            const dados = {
                escolha: formData.get('escolha'),
                tipo: formData.get('tipo'),
                valor: parseFloat(formData.get('valor')),
                taxa: parseFloat(formData.get('taxa')),
                prazo: parseInt(formData.get('prazo')),
                cdi: parseFloat(formData.get('cdi'))
            };

            // Validar dados
            if (!dados.escolha || !dados.tipo || !dados.valor || !dados.taxa || !dados.prazo || !dados.cdi) {
                throw new Error('Por favor, preencha todos os campos.');
            }

            if (dados.valor <= 0 || dados.taxa <= 0 || dados.prazo <= 0 || dados.cdi <= 0) {
                throw new Error('Todos os valores devem ser maiores que zero.');
            }

            // Enviar para a API
            const response = await fetch('https://calculadora-investimentos-backend.onrender.com/calcular', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(dados)
            });

            if (!response.ok) {
                throw new Error('Erro na comunicação com o servidor.');
            }

            const resultado = await response.json();

            if (resultado.erro) {
                throw new Error(resultado.erro);
            }

            // Exibir resultados
            document.getElementById('ganhoNominal').textContent = formatarMoeda(resultado.ganho_nominal);
            document.getElementById('valorFinal').textContent = formatarMoeda(resultado.valor_final);
            
            // Mostrar IR apenas para CDB
            if (dados.escolha.toUpperCase() === 'CDB') {
                document.getElementById('irPago').textContent = formatarMoeda(resultado.ir_pago);
                irContainer.style.display = 'flex';
            } else {
                irContainer.style.display = 'none';
            }

            resultadoContainer.style.display = 'block';

        } catch (error) {
            // Exibir erro
            document.getElementById('mensagemErro').textContent = error.message;
            erroContainer.style.display = 'block';
        } finally {
            // Restaurar botão
            btnCalcular.textContent = originalText;
            btnCalcular.disabled = false;
        }
    });

    // Função para formatar moeda
    function formatarMoeda(valor) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(valor);
    }

    // Adicionar máscara de moeda no campo valor
    const campoValor = document.getElementById('valor');
    campoValor.addEventListener('input', function(e) {
        let valor = e.target.value.replace(/\D/g, '');
        if (valor) {
            valor = (parseFloat(valor) / 100).toFixed(2);
            e.target.value = valor;
        }
    });

    // Adicionar validação em tempo real
    const campos = form.querySelectorAll('input, select');
    campos.forEach(campo => {
        campo.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value) {
                this.style.borderColor = '#dc3545';
            } else {
                this.style.borderColor = '#e1e5e9';
            }
        });
    });
});
