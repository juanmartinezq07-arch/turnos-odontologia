# Spec Delta

## MODIFIED Requirements

### Requirement: Formato de error estable y mapeo de constraints

Todo error SHALL usar la forma `{code, message}`; la violación de EXCLUDE SHALL mapearse a 409 con `RN02_PROFESIONAL` / `RN02_SILLON` y la violación del índice único parcial `rn05_un_activo_por_dia` SHALL mapearse a 409 con `RN05` (nunca 500, distinguiendo por nombre de constraint/índice, no por parseo del mensaje); los errores Pydantic SHALL mapearse a 422.

#### Scenario: Violación EXCLUDE es 409 con código

- **WHEN** un insert viola el EXCLUDE de sillón bajo concurrencia
- **THEN** la API responde 409 con `code = RN02_SILLON`

#### Scenario: Violación de índice RN05 es 409 con código RN05

- **WHEN** un insert viola el índice único parcial `rn05_un_activo_por_dia`
- **THEN** `conflict_code_from_integrity_error` retorna `RN05` y la API responde 409 con `code = RN05`
