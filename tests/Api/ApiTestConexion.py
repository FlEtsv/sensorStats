import unittest
from unittest.mock import patch
from app import app

class ApiTest(unittest.TestCase):
    def setUp(self):
        """Configura el cliente de prueba para la aplicación Flask."""
        self.app = app.test_client()
        self.app.testing = True

    @patch('auxiliar.Api.conexion.chequeoSalud', return_value=True)
    def test_alive_returns_status_alive(self, mock_chequeoSalud):
        """Prueba que el método GET /alive devuelve el estado 'alive'."""
        response = self.app.get('/alive')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "alive"})

    @patch('auxiliar.Api.conexion.chequeoSalud', return_value=False)
    def test_alive_returns_status_not_alive(self, mock_chequeoSalud):
        """Prueba que el método GET /alive devuelve el estado 'not alive' cuando hay problemas."""
        response = self.app.get('/alive')
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json, {"status": "not alive"})

    @patch('auxiliar.Api.conexion.chequeoSalud', side_effect=Exception("Test exception"))
    def test_alive_handles_exception(self, mock_chequeoSalud):
        """Prueba que el método GET /alive maneja excepciones correctamente."""
        response = self.app.get('/alive')
        self.assertEqual(response.status_code, 500)
        self.assertIn("not alive", response.json["status"])
        self.assertIn("error", response.json)

if __name__ == '__main__':
    unittest.main()