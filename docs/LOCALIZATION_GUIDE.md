# Ethiopian Multilingual Localization Architecture

## Supported National Languages
1. **Amharic (አማርኛ) - `am`**: National working language, Ge'ez script.
2. **English (English) - `en`**: Administrative and inter-agency working language.
3. **Afaan Oromoo - `om`**: Latin (Qubee) script.
4. **Tigrinya (ትግርኛ) - `ti`**: Ge'ez script.

## Ethiopic Calendar (ባህረ ሃሳብ) Integration
The platform stores all timestamps internally in ISO 8601 UTC. For UI presentation and field officer reports, dates are bi-directionally convertible between Gregorian and the Ethiopian calendar (Meskerem to Pagume, 7-8 years difference).

## Voice Note Ingestion
Field voice notes captured in rural zones are encoded in AAC/M4A format and transcribed via regional speech recognition acoustic models.
