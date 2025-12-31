import json
import base64
from django.contrib.auth import get_user_model
from patients.models import Appointment
from doctors.models import Doctor

User = get_user_model()

# Create a dummy user
user, created = User.objects.get_or_create(username='testpatient_e2e', defaults={'email': 'test_e2e@example.com'})
if created:
    user.set_password('testpassword')
    user.save()

# Create a dummy profile for the user
from users.models import Profile
profile, created = Profile.objects.get_or_create(user=user, defaults={'role': 'patient'})
profile.save()

# Create a dummy doctor
doctor, created = Doctor.objects.get_or_create(user=user, defaults={'specialty': 'General'})

# Create an Appointment with encrypted fields
symptoms_text = "Severe headache and nausea"
preferred_date_text = "2025-12-30"
preferred_time_text = "14:30:00"

appointment = Appointment.objects.create(
    patient=user,
    doctor=doctor,
    symptoms=symptoms_text,
    preferred_date=preferred_date_text,
    preferred_time=preferred_time_text,
)
appointment.save()

print(f"Created Appointment ID: {appointment.id}")
with open('encrypted_data_debug.json', 'w') as f:
    f.write(appointment.encrypted_data)
print("Encrypted data written to encrypted_data_debug.json")

# Retrieve the Appointment and verify decryption
retrieved_appointment = Appointment.objects.get(id=appointment.id)

print(f"Retrieved Symptoms (decrypted): {retrieved_appointment.symptoms}")
print(f"Retrieved Preferred Date (decrypted): {retrieved_appointment.preferred_date}")
print(f"Retrieved Preferred Time (decrypted): {retrieved_appointment.preferred_time}")

# Assertions to verify decryption
assert retrieved_appointment.symptoms == symptoms_text
assert retrieved_appointment.preferred_date == preferred_date_text
assert retrieved_appointment.preferred_time == preferred_time_text

print("End-to-end encryption/decryption test successful!")

# Clean up: delete the created appointment and user/doctor if they were just created
appointment.delete()
if created:
    user.delete()
    doctor.delete()