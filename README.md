Irrigation Time Management System
This Django-based application is designed to help farmers efficiently manage irrigation schedules. The app dynamically adjusts irrigation times based on various factors and checks the status of water wells by receiving SMS updates from well sensors. It ensures optimized irrigation schedules and provides notifications to farmers via SMS.

Key features:

Dynamic irrigation scheduling: Adjusts irrigation times based on various conditions.
Well status monitoring: Monitors the status of water wells (on/off) through SMS updates from well sensors or via the Flutter-based app.
Task management: Uses Celery and Celery Beat to schedule and manage tasks such as sending notifications and updating irrigation times.
Notification system: Sends SMS alerts to farmers to keep them informed about their irrigation schedules and well status.

For the Flutter-based app that uses this API, please visit the repository at: https://github.com/alishams23/Irrigation-time

