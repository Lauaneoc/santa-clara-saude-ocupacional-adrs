# Architecture Decision Records (ADRs)
## Clínica Santa Clara – Saúde Ocupacional

---

## ADR-01: Adoção do Estilo Arquitetural N-Camadas

### Contexto
O sistema possui múltiplos módulos de cadastro e regras de negócio específicas. Os requisitos não funcionais relacionados à organização, manutenção e separação de responsabilidades indicam a necessidade de uma arquitetura estruturada.

### Decisão
Adotar o estilo arquitetural N-Camadas, dividido em Camada de Apresentação, Camada de Negócio e Camada de Dados.

### Status
Aceita

### Consequências
- **Positiva:** melhor separação de responsabilidades e maior facilidade de manutenção.
- **Negativa:** aumento da complexidade estrutural e possível aumento no tempo de resposta entre camadas.

---

## ADR-02: Integração com APIs Externas para Validação

### Contexto
Os requisitos funcionais exigem validação de CPF, CNPJ, CEP e CRM durante os cadastros realizados no sistema.

### Decisão
Integrar o backend com APIs externas responsáveis pela validação das informações fornecidas pelos usuários.

### Status
Aceita

### Consequências
- **Positiva:** maior confiabilidade e veracidade dos dados cadastrados.
- **Negativa:** dependência de serviços externos e possibilidade de indisponibilidade das APIs.

---

## ADR-03: Autenticação com E-mail e Senha

### Contexto
O sistema manipula informações sensíveis relacionadas à saúde ocupacional, tornando necessário restringir o acesso apenas a usuários autorizados. Além disso, o sistema deverá se adequar à LGPD, garantindo maior proteção e controle sobre os dados pessoais armazenados.

### Decisão
Implementar autenticação utilizando e-mail e senha com armazenamento seguro por meio de hash, além da adoção de mecanismos que auxiliem na obediência às regras e restrições impostas pela LGPD relacionadas à proteção de dados pessoais e controle de acesso às informações sensíveis do sistema.

### Status
Aceita

### Consequências
- **Positiva:** maior segurança no armazenamento das credenciais dos usuários.
- **Negativa:** necessidade de gerenciamento de sessão e maior complexidade no backend.

---

## ADR-04: Uso de Integridade Referencial

### Contexto
Os agendamentos dependem da existência prévia de empresas, pacientes e exames cadastrados no sistema.

### Decisão
Aplicar validações referenciais na camada de negócio e utilizar chaves estrangeiras no banco de dados relacional.

### Status
Aceita

### Consequências
- **Positiva:** maior consistência e integridade das informações armazenadas.
- **Negativa:** aumento da quantidade de validações e consultas realizadas antes da persistência.

---

## ADR-05: Interface Web Baseada em Componentes Padrão

### Contexto
Os requisitos não funcionais estabelecem a necessidade de uma interface amigável e baseada em componentes Web.

### Decisão
Utilizar componentes web padrão como formulários, tabelas, modais e mensagens de feedback visual.

### Status
Aceita

### Consequências
- **Positiva:** facilidade de uso e melhor experiência para os usuários.
- **Negativa:** menor flexibilidade visual e limitação de personalizações avançadas.

---

## ADR-06: Utilização de Banco de Dados Relacional

### Contexto
O sistema possui entidades fortemente relacionadas, como Empresa, Paciente, Médico, Exame e Agendamento.

### Decisão
Adotar o PostgreSQL como banco de dados relacional, com uso de chaves primárias, chaves estrangeiras e índices nos campos de busca (CNPJ, CPF, CRM, código de exame).

### Status
Aceita

### Consequências
- **Positiva:** suporte eficiente a relacionamentos e maior integridade dos dados.
- **Negativa:** maior rigidez estrutural para alterações futuras no esquema do banco.
