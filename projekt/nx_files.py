# -*- coding: utf-8 -*-
"""SX35Z v4.8: native .prt creation/save, restricted to THIS journal run.

No SaveAs, overwrite, deletion, automatic close, or SaveAll is used. Each part
is created using its final absolute pathname; only that registered part is
saved with SaveComponents=False. The containing folder AND every basename
include a run identifier. This module must run inside Siemens NX.

NX is not executed by the companion offline tests: they use explicit doubles.
"""
import ntpath
import os
import re
import json
from uuid import uuid4
import NXOpen

FILES_VERSION = '4.8'


def canonical(path):
    """Local native path identity (resolves case on Windows and symlinks)."""
    return os.path.normcase(os.path.realpath(os.path.abspath(os.fspath(path))))


def default_output_root():
    """Separate output from the script drive. Never guess a fixed username."""
    base = os.environ.get('LOCALAPPDATA') or os.path.expanduser('~')
    if not base or base == '~' or not os.path.isabs(base):
        raise RuntimeError('Kein absoluter Benutzerpfad fuer die lokale Ausgabe gefunden. '
                           'NX_Ausgabe.json mit absolutem output_root anlegen.')
    return os.path.abspath(os.path.join(base, 'SX35Z', 'NX_Output'))


def select_output_root(journal_directory, log=None):
    """Read optional NX_Ausgabe.json; empty/missing means per-user local output.

    An explicitly chosen failing destination is NEVER silently replaced. The
    input scripts and Parameter.json stay in their original directory.
    """
    emit = log if log is not None else (lambda text: None)
    config = os.path.join(journal_directory, 'NX_Ausgabe.json')
    try:
        with open(config, encoding='utf-8-sig') as stream:
            data = json.load(stream)
    except FileNotFoundError:
        data = {}
    if not isinstance(data, dict) or set(data) - {'output_root'}:
        raise ValueError('NX_Ausgabe.json: Objekt mit einzigem optionalem Feld output_root erwartet.')
    value = data.get('output_root', '')
    if not isinstance(value, str):
        raise ValueError('NX_Ausgabe.json: output_root muss Text sein.')
    if value.strip():
        root = os.path.expanduser(os.path.expandvars(value.strip()))
        if not os.path.isabs(root):
            raise ValueError('NX_Ausgabe.json: output_root muss absolut sein.')
        # ntpath.isabs also accepts a drive-relative root such as \folder on
        # Python 3.10; do not let the session current drive decide the output.
        if os.name == 'nt' and not ntpath.splitdrive(root)[0]:
            raise ValueError('NX_Ausgabe.json: vollstaendiger absoluter Laufwerks- oder UNC-Pfad erforderlich.')
        root = os.path.abspath(root)
        emit('Ausgabeziel aus NX_Ausgabe.json: ' + root)
    else:
        root = default_output_root()
        emit('Standardausgabe im Benutzerprofil, unabhaengig vom Journalordner: ' + root)
    return root


def _verify_file_io(directory):
    """Exclusive probe file: write, flush, read back, rename, and remove OWN file.

    This is a Python filesystem test, not proof of NX .prt Save/AddComponent.
    """
    probe_id = uuid4().hex
    name = os.path.join(directory, '.sx35z_probe_' + probe_id + '.tmp')
    renamed = os.path.join(directory, '.sx35z_probe_' + probe_id + '_moved.tmp')
    payload = ('SX35Z IO probe ' + probe_id).encode('ascii')
    owned = None
    try:
        with open(name, 'xb') as stream:
            owned = name
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        with open(name, 'rb') as stream:
            if stream.read() != payload:
                raise RuntimeError('Pfadtest: gelesene Daten stimmen nicht mit geschriebenen Daten ueberein.')
        if os.path.lexists(renamed):
            raise FileExistsError('Unerwartete Datei am exklusiven Probe-Umbenennungsziel: ' + renamed)
        os.rename(name, renamed)
        owned = renamed
        with open(renamed, 'rb') as stream:
            if stream.read() != payload:
                raise RuntimeError('Pfadtest: Daten nach Umbenennen veraendert.')
    finally:
        if owned is not None:
            os.remove(owned)


def prepare_output_directory(journal_directory, run_name, log=None):
    """Create one new, checked run folder BEFORE creating any native NX part."""
    emit = log if log is not None else (lambda text: None)
    if not re.fullmatch(r'[A-Za-z0-9_-]+', str(run_name)):
        raise ValueError('Ungueltiger Laufordnername: ' + str(run_name))
    root = select_output_root(journal_directory, emit)
    emit('Journal-/Eingabeordner: ' + os.path.abspath(journal_directory))
    emit('Geplante Ausgabe: ' + os.path.join(root, run_name))
    out = None
    try:
        os.makedirs(root, exist_ok=True)
        # Do NOT ignore WinError1005 or replace realpath by string-only
        # normalisation. Canonical identity guards links/foreign output paths.
        root = canonical(root)
        out = os.path.join(root, run_name)
        os.mkdir(out)  # exclusive; never reuse an older run directory
        out = canonical(out)
        _verify_file_io(out)
    except FileExistsError:
        raise
    except (OSError, RuntimeError) as exc:
        code = getattr(exc, 'winerror', None)
        emit('Pfadtest fehlgeschlagen: Ziel=%r; Typ=%s; WinError=%r; errno=%r; %s' %
             (out or root, type(exc).__name__, code, getattr(exc, 'errno', None), exc))
        raise RuntimeError('Ausgabeordner nicht verwendbar: %s; WinError=%r; %s. '
                           'In NX_Ausgabe.json output_root auf einen beschreibbaren lokalen '
                           'Ordner setzen oder leer lassen. Keine NX-Teile erzeugt; '
                           'kein stiller Wechsel auf ein anderes Ziel.' %
                           (out or root, code, exc)) from exc
    with open(os.path.join(out, 'NX_Pfadpruefung.json'), 'x', encoding='utf8') as stream:
        json.dump(dict(journal_directory=os.path.abspath(journal_directory),
                       output_directory=out, io_probe_passed=True,
                       tested=['realpath', 'exclusive_write', 'flush_fsync', 'read', 'rename', 'delete_own_probe'],
                       nx_save_verified=False), stream, indent=2)
    emit('Pfadtest bestanden: Aufloesen, Schreiben, Ruecklesen, Umbenennen und Entfernen der eigenen Testdatei.')
    emit('Ausgabeordner: ' + out)
    return out


def leaf_key(path):
    """NX filename comparison, independent of directory, separator and case."""
    name = ntpath.basename(str(path).rstrip('/\\'))
    if name.lower().endswith('.prt'):
        name = name[:-4]
    return name.casefold()


def _text(obj, name):
    try:
        return str(getattr(obj, name))
    except Exception as exc:
        return '<%s nicht lesbar: %s>' % (name, exc)


def _signature(path):
    s = os.stat(path)
    return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns)


def _consume_save_status(status, log):
    """Do not discard reported save failures when NX returns without raising."""
    if status is None:
        log('Save lieferte keinen Status; Zielpfad und Dateigroesse werden geprueft.')
        return
    try:
        n = int(status.NumberUnsavedParts)
        m = int(getattr(status, 'NumberUnsavedObjects', 0))
        details = []
        for i in range(n):
            try:
                details.append('Teil %s; Fehlercode %s' %
                               (_text(status.GetPart(i), 'FullPath'), status.GetStatus(i)))
            except Exception as exc:
                details.append('Status %d nicht voll lesbar: %s' % (i, exc))
        for i in range(m):
            try:
                details.append('Objektfehlercode %s' % status.GetObjectStatus(i))
            except Exception as exc:
                details.append('Objektstatus %d nicht lesbar: %s' % (i, exc))
        log('Speicherstatus: ungespeicherte Teile=%d, Objekte=%d' % (n, m))
        if n or m:
            raise RuntimeError('NX meldet ungespeicherte Daten: ' + '; '.join(details))
    finally:
        status.Dispose()


class NativePartFiles:
    """Keep ownership of newly created parts; never save a pre-existing part.

    ``creator(path)`` must call Parts.NewDisplay(path, Part.Units.Millimeters)
    and validate units/history. Registrations belong to this Python instance,
    not to a global registry retained between journal runs.
    """
    def __init__(self, session, directory, run_id, log=None):
        self.session = session
        self.directory = canonical(directory)
        if not re.fullmatch(r'[A-Za-z0-9_]+', str(run_id)):
            raise ValueError('Ungueltige Lauf-ID')
        self.run_id = str(run_id)
        self.log = log if log is not None else (lambda text: None)
        self.records = {}
        self.last_target = None
        self.last_part = None
        os.makedirs(self.directory, exist_ok=True)

    def filename(self, folder, stem):
        """Use a unique run suffix for tests, parts, subassemblies AND root."""
        if not re.fullmatch(r'[A-Za-z0-9_-]+', str(stem)):
            raise ValueError('Ungueltiger Dateistamm: ' + str(stem))
        folder = canonical(folder)
        path = os.path.join(folder, '%s__%s.prt' % (stem, self.run_id))
        self._check_target(path)
        return path

    def _check_target(self, path):
        path = os.fspath(path)
        if not os.path.isabs(path):
            raise ValueError('Absoluter .prt-Zielpfad erforderlich: ' + path)
        if not path.lower().endswith('.prt'):
            raise ValueError('Ziel muss eine .prt-Datei sein: ' + path)
        if os.path.islink(path):
            raise FileExistsError('Symbolischer Link am Ziel; kein Folgen oder Ueberschreiben: ' + path)
        target = canonical(path)
        try:
            inside = os.path.commonpath([self.directory, target]) == self.directory
        except ValueError:
            inside = False
        if not inside:
            raise ValueError('Ziel liegt ausserhalb dieses Laufordners: ' + path)
        # Local native mode only. No inferred Teamcenter paths.
        if path.startswith('@DB/') or path.startswith('<@>DB/'):
            raise ValueError('Dieses Journal erzeugt lokale native Dateien, keine PDM-Objekte.')
        return target

    def _conflicts(self, path, exclude=None):
        try:
            parts = list(self.session.Parts)
        except Exception as exc:
            raise RuntimeError('Offene NX-Teile nicht pruefbar: ' + str(exc)) from exc
        result = []
        wanted = leaf_key(path)
        for part in parts:
            if part is exclude:
                continue
            if exclude is not None:
                # NX may return a second Python wrapper for the same tagged part.
                try:
                    if part.Tag == exclude.Tag:
                        continue
                except Exception:
                    pass
            found = False
            for prop in ('FullPath', 'Leaf'):
                try:
                    text = str(getattr(part, prop))
                except Exception:
                    continue
                if text and leaf_key(text) == wanted:
                    found = True
            if found:
                result.append(part)
        return result

    def diagnose(self, part=None, path=None, exception=None):
        """Read-only diagnostics. Never turn a failed save into success."""
        part = part if part is not None else self.last_part
        path = path if path is not None else self.last_target
        self.log('--- Speicherdiagnose v4.8 ---')
        self.log('Vorgesehenes Ziel: ' + str(path))
        if part is not None:
            for prop in ('FullPath', 'Leaf', 'Name', 'Tag', 'IsModified', 'IsReadOnly'):
                self.log('NX %s: %s' % (prop, _text(part, prop)))
        if path:
            try:
                self.log('Datentraeger: existiert=%s; Datei=%s; Groesse=%s' %
                         (os.path.lexists(path), os.path.isfile(path),
                          os.path.getsize(path) if os.path.isfile(path) else 'n/a'))
                for other in self._conflicts(path, part):
                    self.log('Namenskonflikt in Sitzung: ' + _text(other, 'FullPath'))
            except Exception as exc:
                self.log('Zusatzdiagnose fehlgeschlagen: ' + str(exc))
        if exception is not None:
            self.log('Ausnahme: %s: %s' % (type(exception).__name__, exception))
            self.log('NX Fehlercode, falls vorhanden: ' + _text(exception, 'ErrorCode'))

    def create(self, path, creator):
        path = self._check_target(path)
        self.last_target = path
        self.last_part = None
        self.log('Neues NX-Teil am endgueltigen Ziel: ' + path)
        try:
            if path in self.records:
                raise RuntimeError('Ziel bereits in diesem Lauf registriert: ' + path)
            if os.path.lexists(path):
                raise FileExistsError('Zieldatei existiert bereits; kein Ueberschreiben: ' + path)
            conflicts = self._conflicts(path)
            if conflicts:
                raise RuntimeError('Gleicher Teilename bereits in NX geladen: ' +
                                   '; '.join(_text(p, 'FullPath') for p in conflicts))
            os.makedirs(os.path.dirname(path), exist_ok=True)
            part = creator(path)
            self.last_part = part
            if part is None:
                raise RuntimeError('NewDisplay lieferte kein Teil.')
            actual = str(part.FullPath)
            if not actual or not os.path.isabs(actual) or canonical(actual) != path:
                raise RuntimeError('NewDisplay hat das erwartete Dateiziel nicht gesetzt: '
                                   'FullPath=%r; Ziel=%r. Kein SaveAs-Fallback.' % (actual, path))
            # Normally NewDisplay assigns a path without writing a disk file.
            # If NX does write during creation, record only this newly born file.
            signature = _signature(path) if os.path.isfile(path) else None
            self.records[path] = {'part': part, 'signature': signature, 'saved': False}
            self.log('NX FullPath bestaetigt: ' + actual)
            return part
        except Exception as exc:
            self.diagnose(exception=exc)
            raise

    def save(self, part, path):
        path = self._check_target(path)
        self.last_target, self.last_part = path, part
        self.log('Speichern mit Save, ohne SaveAs: ' + path)
        try:
            record = self.records.get(path)
            if record is None or record['part'] is not part:
                raise RuntimeError('Teil nicht von diesem Lauf erzeugt; Speichern verweigert.')
            actual = str(part.FullPath)
            if not actual or not os.path.isabs(actual) or canonical(actual) != path:
                raise RuntimeError('Teilpfad hat sich geaendert; kein Speichern an fremdem Ziel: '
                                   + repr(actual))
            if self._conflicts(path, part):
                raise RuntimeError('Anderes geladenes Teil mit demselben Dateinamen; Abbruch.')
            if os.path.lexists(path):
                if (not os.path.isfile(path) or record['signature'] is None or
                        _signature(path) != record['signature']):
                    raise FileExistsError('Ziel wurde ausserhalb dieses Speichervorgangs '
                                          'angelegt/geaendert; kein Ueberschreiben: ' + path)
            elif record['signature'] is not None:
                raise RuntimeError('Die zuvor gespeicherte Datei fehlt; Abbruch: ' + path)
            status = part.Save(NXOpen.BasePart.SaveComponents.FalseValue,
                               NXOpen.BasePart.CloseAfterSave.FalseValue)
            _consume_save_status(status, self.log)
            actual = str(part.FullPath)
            if canonical(actual) != path:
                raise RuntimeError('NX-Teilpfad nach Save unerwartet: ' + repr(actual))
            if not os.path.isfile(path) or os.path.getsize(path) <= 0:
                raise RuntimeError('Save hat keine nichtleere Zieldatei erzeugt: ' + path)
            record['signature'] = _signature(path)
            record['saved'] = True
            self.log('Gespeichert und Dateiexistenz geprueft: %s (%d Bytes)' %
                     (path, os.path.getsize(path)))
            return path
        except Exception as exc:
            self.diagnose(exception=exc)
            raise
