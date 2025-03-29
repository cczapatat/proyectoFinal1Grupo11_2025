from dataclasses import dataclass, field
from typing import Dict, Any
from ..models.seller_model import CURRENCY, SELLER_ZONE
import uuid
import re

@dataclass
class SellerDTO:
    user_id: str = field(default=None)
    name: str = field(default=None)
    phone: str = field(default=None)
    email: str = field(default=None)
    zone: str = field(default=None)
    quota_expected: float = field(default=None)
    currency_quota: str = field(default=None)
    quartely_target: float = field(default=None)
    currency_target: str = field(default=None)
    performance_recomendations: str = field(default=None)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SellerDTO':
        cls._validate_required_fields(data)
        cls._validate_field_types(data)
        
        cls._validate_user_id(data['user_id'])
        cls._validate_phone(data['phone'])
        cls._validate_email(data['email'])
        cls._validate_zone(data['zone'])
        cls._validate_currencies(data['currency_quota'], data['currency_target'])
        cls._validate_numeric_fields(data['quota_expected'], data['quartely_target'])
        cls._validate_text_fields(data['name'], data['performance_recomendations'])
        
        filtered_data = {
            k: v for k, v in data.items()
            if hasattr(cls, k)
        }
        return cls(**filtered_data)
        
    @staticmethod
    def _validate_required_fields(data: Dict[str, Any]) -> None:
        required_fields = [
            'user_id', 'name', 'phone', 'email', 'zone',
            'quota_expected', 'currency_quota', 'quartely_target',
            'currency_target', 'performance_recomendations'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Campos requeridos faltantes: {', '.join(missing_fields)}")
            
    @staticmethod
    def _validate_field_types(data: Dict[str, Any]) -> None:
        type_validations = {
            'user_id': (str, "El ID de usuario debe ser una cadena de texto"),
            'name': (str, "El nombre debe ser una cadena de texto"),
            'phone': (str, "El teléfono debe ser una cadena de texto"),
            'email': (str, "El email debe ser una cadena de texto"),
            'zone': (str, "La zona debe ser una cadena de texto"),
            'quota_expected': ((int, float), "La cuota esperada debe ser un número"),
            'currency_quota': (str, "La moneda de la cuota debe ser una cadena de texto"),
            'quartely_target': ((int, float), "El objetivo trimestral debe ser un número"),
            'currency_target': (str, "La moneda del objetivo debe ser una cadena de texto"),
            'performance_recomendations': (str, "Las recomendaciones de desempeño deben ser una cadena de texto")
        }
        
        errors = []
        for field, (expected_type, error_msg) in type_validations.items():
            if field in data and not isinstance(data[field], expected_type):
                errors.append(error_msg)
                
        if errors:
            raise ValueError(f"Errores de validación de tipo: {'; '.join(errors)}")
            
    @staticmethod
    def _validate_user_id(user_id: str) -> None:
        try:
            uuid.UUID(user_id)
        except (ValueError, AttributeError, TypeError):
            raise ValueError("Formato UUID inválido para user_id. Por favor proporcione un UUID válido.")
            
    @staticmethod
    def _validate_phone(phone: str) -> None:
        if not isinstance(phone, str) or not re.match(r'^\+[1-9][0-9]{1,14}$', phone):
            raise ValueError("Formato de teléfono inválido. Debe comenzar con + seguido de 1-14 dígitos (ej., +123456789)")
            
    @staticmethod
    def _validate_email(email: str) -> None:
        if not isinstance(email, str) or not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            raise ValueError("Formato de email inválido. Por favor proporcione una dirección de correo válida (ej., usuario@ejemplo.com)")
            
    @staticmethod
    def _validate_zone(zone: str) -> None:
        try:
            SELLER_ZONE(zone)
        except ValueError:
            valid_zones = ", ".join([f"'{z.value}'" for z in SELLER_ZONE])
            raise ValueError(f"Zona inválida: '{zone}'. Debe ser uno de: {valid_zones}")
            
    @staticmethod
    def _validate_currencies(currency_quota: str, currency_target: str) -> None:
        valid_currencies = ", ".join([f"'{c.value}'" for c in CURRENCY])
        errors = []
        
        try:
            CURRENCY(currency_quota)
        except ValueError:
            errors.append(f"Moneda de cuota inválida: '{currency_quota}'")
        
        try:
            CURRENCY(currency_target)
        except ValueError:
            errors.append(f"Moneda de objetivo inválida: '{currency_target}'")
            
        if errors:
            error_msg = "; ".join(errors)
            raise ValueError(f"{error_msg}. Las monedas válidas son: {valid_currencies}")
            
    @staticmethod
    def _validate_numeric_fields(quota_expected: float, quartely_target: float) -> None:
        errors = []
        
        if not isinstance(quota_expected, (int, float)):
            errors.append("La cuota esperada debe ser un número")
        elif quota_expected <= 0:
            errors.append("La cuota esperada debe ser un número positivo mayor que cero")
            
        if not isinstance(quartely_target, (int, float)):
            errors.append("El objetivo trimestral debe ser un número")
        elif quartely_target <= 0:
            errors.append("El objetivo trimestral debe ser un número positivo mayor que cero")
            
        if errors:
            raise ValueError(f"Errores de validación en campos numéricos: {'; '.join(errors)}")
            
    @staticmethod
    def _validate_text_fields(name: str, performance_recomendations: str) -> None:
        errors = []
        
        if not name or not isinstance(name, str):
            errors.append("El nombre debe ser una cadena de texto no vacía")
        elif len(name) > 100:
            errors.append("El nombre no debe exceder los 100 caracteres")
            
        if not isinstance(performance_recomendations, str):
            errors.append("Las recomendaciones de desempeño deben ser una cadena de texto")
        elif len(performance_recomendations) > 255:
            errors.append("Las recomendaciones de desempeño no deben exceder los 255 caracteres")
            
        if errors:
            raise ValueError(f"Errores de validación en campos de texto: {'; '.join(errors)}")

    def to_dict(self) -> Dict[str, Any]:
        return {
            k: v for k, v in self.__dict__.items()
            if v is not None
        }
