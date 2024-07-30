import unittest
from unittest.mock import patch, mock_open, MagicMock

import requests
from flask import Flask
import json
import os
from app import app, get_data

class AppTestCase(unittest.TestCase):
    def setUp(self):
        """Configura el cliente de prueba para la aplicación Flask."""
        self.app = app.test_client()
        self.app.testing = True

    @patch('requests.get')
    def get_data_returns_json_on_success(self, mock_get):
        """Prueba que get_data devuelve JSON en caso de éxito."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'key': 'value'}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_data('http://example.com')
        self.assertEqual(result, {'key': 'value'})

    @patch('requests.get')
    def get_data_returns_none_on_request_exception(self, mock_get):
        """Prueba que get_data devuelve None en caso de excepción de solicitud."""
        mock_get.side_effect = requests.RequestException("API error")

        result = get_data('http://example.com')
        self.assertIsNone(result)

    @patch('requests.get')
    def get_data_handles_http_error(self, mock_get):
        """Prueba que get_data maneja errores HTTP correctamente."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.HTTPError("HTTP error")
        mock_get.return_value = mock_response

        result = get_data('http://example.com')
        self.assertIsNone(result)

    @patch('requests.get')
    def get_data_handles_invalid_json(self, mock_get):
        """Prueba que get_data maneja JSON inválido correctamente."""
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_data('http://example.com')
        self.assertIsNone(result)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs', return_value=None)
    @patch('auxiliar.utilidades.construirAPI', return_value='http://127.0.0.1/get_vehicleinfo/12345?from_cache=1')
    @patch('auxiliar.data.get_data_boolean', return_value=True)
    def connect_post_saves_data(self, mock_get_data_boolean, mock_construirAPI, mock_makedirs, mock_exists, mock_open):
        """Prueba que el método POST /connect guarda los datos correctamente."""
        response = self.app.post('/connect', data={'ip_port': '127.0.0.1', 'vin': '12345'})
        self.assertEqual(response.status_code, 302)
        mock_open().write.assert_called_once_with('{"ip_port": "127.0.0.1", "vin": "12345"}')

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs', return_value=None)
    @patch('auxiliar.utilidades.construirAPI', return_value='http://127.0.0.1/get_vehicleinfo/12345?from_cache=1')
    @patch('auxiliar.data.get_data_boolean', return_value=False)
    def connect_post_handles_api_error(self, mock_get_data_boolean, mock_construirAPI, mock_makedirs, mock_exists, mock_open):
        """Prueba que el método POST /connect maneja errores de API correctamente."""
        response = self.app.post('/connect', data={'ip_port': '127.0.0.1', 'vin': '12345'})
        self.assertEqual(response.status_code, 302)
        mock_open().write.assert_not_called()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.makedirs', return_value=None)
    @patch('auxiliar.utilidades.construirAPI', return_value='http://127.0.0.1/get_vehicleinfo/12345?from_cache=1')
    @patch('auxiliar.data.get_data_boolean', return_value=True)
    def connect_post_handles_exception(self, mock_get_data_boolean, mock_construirAPI, mock_makedirs, mock_exists, mock_open):
        """Prueba que el método POST /connect maneja excepciones correctamente."""
        mock_open.side_effect = Exception("File write error")
        response = self.app.post('/connect', data={'ip_port': '127.0.0.1', 'vin': '12345'})
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Error saving data', response.data)

    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    @patch('os.path.exists', return_value=True)
    def test_index_get_with_empty_data(self, mock_exists, mock_open):
        """Prueba que el método GET / maneja datos vacíos correctamente."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error obteniendo los datos', response.data)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=False)
    def test_index_get_creates_file_if_not_exists(self, mock_exists, mock_open):
        """Prueba que el método GET / crea el archivo si no existe."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        mock_open.assert_any_call('data/historialDatos/data.json', 'w')
        mock_open().write.assert_called_once_with('{}')

    @patch('auxiliar.utilidades.construirAPI')
    @patch('auxiliar.data.get_data')
    def test_index_get_with_api_error(self, mock_get_data, mock_construirAPI):
        """Prueba que el método GET / maneja errores de API correctamente."""
        mock_construirAPI.return_value = 'http://127.0.0.1/get_vehicleinfo/12345?from_cache=1'
        mock_get_data.return_value = None
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Error obteniendo los datos', response.data.decode('utf-8'))

    @patch('builtins.open', new_callable=mock_open, read_data='{"ip_port": "127.0.0.1", "vin": "12345"}')
    @patch('os.path.exists', return_value=True)
    @patch('app.get_data', return_value={'battery': {'voltage': 12}})
    def test_get_data_bot(self, mock_get_data, mock_exists, mock_open):
        """Prueba que el método GET /get_data_bot obtiene datos correctamente."""
        response = self.app.get('/get_data_bot')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'12', response.data)

    @patch('builtins.open', new_callable=mock_open, read_data='{"ip_port": "127.0.0.1", "vin": "12345"}')
    @patch('os.path.exists', return_value=True)
    @patch('app.get_data', return_value=None)
    def test_get_data_bot_with_api_error(self, mock_get_data, mock_exists, mock_open):
        """Prueba que el método GET /get_data_bot maneja errores de API correctamente."""
        response = self.app.get('/get_data_bot')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Error obteniendo los datos', response.data)

if __name__ == '__main__':
    unittest.main()