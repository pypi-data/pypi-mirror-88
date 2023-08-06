from datetime import datetime, timedelta
from unittest import TestCase
from unittest.mock import patch, MagicMock

from pysmoothstreams import Server, Quality, Protocol, Service, Feed
from pysmoothstreams.auth import AuthSign
from pysmoothstreams.exceptions import (
    InvalidServer,
    InvalidQuality,
    InvalidProtocol,
    InvalidContentType,
)
from pysmoothstreams.guide import Guide


class TestGuide(TestCase):
    @patch("urllib.request.urlopen")
    def setUp(self, mock_urlopen):
        with open("./tests/test_altepg1.xml", "r") as f:
            json_feed = f.read()

        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.read.return_value = json_feed.encode()
        cm.info.return_value = {
            "Expires": "Sat, 25 Aug 2018 22:39:41 GMT",
            "Content-Type": "text/xml",
        }
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.g = Guide(Feed.SMOOTHSTREAMS)

    def test_build_stream_url_live247_rtmp(self):
        a = AuthSign(service=Service.LIVE247, auth=("fake", "fake"))
        # set hash and expiration manually
        a.expiration_date = datetime.now() + timedelta(minutes=240)
        a.hash = "abc1234"

        generated = self.g.build_stream_url(
            Server.NA_EAST_NY, 44, a, Quality.HD, Protocol.RTMP
        )

        self.assertEqual(
            "rtmp://dnae2.smoothstreams.tv:3625/view247/ch44q1.stream/playlist.m3u8?wmsAuthSign=abc1234",
            generated,
        )

    def test_build_stream_url_streamtvnow_hls(self):
        a = AuthSign(service=Service.STREAMTVNOW, auth=("fake", "fake"))
        # set hash and expiration manually
        a.expiration_date = datetime.now() + timedelta(minutes=240)
        a.hash = "abc1234"

        generated = self.g.build_stream_url(
            Server.ASIA_MIX, 10, a, Quality.LQ, Protocol.HLS
        )

        self.assertEqual(
            "https://dAP.smoothstreams.tv:443/viewstvn/ch10q3.stream/playlist.m3u8?wmsAuthSign=abc1234",
            generated,
        )

    def test_build_stream_url_streamtvnow_mpeg(self):
        a = AuthSign(service=Service.STREAMTVNOW, auth=("fake", "fake"))
        # set hash and expiration manually
        a.expiration_date = datetime.now() + timedelta(minutes=240)
        a.hash = "abc1234"

        generated = self.g.build_stream_url(
            Server.EU_MIX, 3, a, Quality.LQ, Protocol.MPEG
        )

        self.assertEqual(
            "https://deu.smoothstreams.tv:443/viewstvn/ch03q3.stream/mpeg.2ts?wmsAuthSign=abc1234",
            generated,
        )

    def test_build_stream_url_rtsp(self):
        a = AuthSign(service=Service.STREAMTVNOW, auth=("fake", "fake"))
        a.expiration_date = datetime.now() + timedelta(minutes=240)
        a.hash = "abc1234"

        generated = self.g.build_stream_url(
            Server.EU_MIX, 3, a, Quality.LQ, Protocol.RTSP
        )

        self.assertEqual(
            "rtsp://deu.smoothstreams.tv:2935/viewstvn/ch03q3.stream/playlist.m3u8?wmsAuthSign=abc1234",
            generated,
        )

    def test_build_stream_url_live247_dash(self):
        a = AuthSign(service=Service.LIVE247, auth=("fake", "fake"))
        # set hash and expiration manually
        a.expiration_date = datetime.now() + timedelta(minutes=240)
        a.hash = "abc1234"

        generated = self.g.build_stream_url(
            Server.NA_EAST_NY, 44, a, Quality.HD, Protocol.DASH
        )

        self.assertEqual(
            "https://dnae2.smoothstreams.tv:443/view247/ch44.smil/manifest.mpd?wmsAuthSign=abc1234",
            generated,
        )

    def test_build_stream_url_live247_hls_adaptive(self):
        a = AuthSign(service=Service.LIVE247, auth=("fake", "fake"))
        # set hash and expiration manually
        a.expiration_date = datetime.now() + timedelta(minutes=240)
        a.hash = "abc1234"

        generated = self.g.build_stream_url(
            Server.NA_EAST_NY, 44, a, Quality.HD, Protocol.HLSA
        )

        self.assertEqual(
            "https://dnae2.smoothstreams.tv:443/view247/ch44.smil/playlist.m3u8?wmsAuthSign=abc1234",
            generated,
        )

    def test_generate_streams(self):
        a = AuthSign(service=Service.STREAMTVNOW, auth=("fake", "fake"))

        with self.assertRaises(InvalidServer) as context:
            self.g.generate_streams("FakeServer", Quality.HD, a, protocol=Protocol.HLS)

        self.assertTrue("FakeServer is not a valid server!" in str(context.exception))

        with self.assertRaises(InvalidQuality) as context:
            self.g.generate_streams(Server.EU_MIX, 29, a, protocol=Protocol.HLS)

        self.assertTrue("29 is not a valid quality!" in str(context.exception))

        with self.assertRaises(InvalidProtocol) as context:
            self.g.generate_streams(Server.EU_MIX, Quality.LQ, a, protocol="abc")

        self.assertTrue("abc is not a valid protocol!" in str(context.exception))

    @patch("urllib.request.urlopen")
    def test__fetch_channels(self, mock_urlopen):

        self.assertEqual(150, len(self.g.channels))

        self.assertEqual("ESPNNews", self.g.channels[0]["name"])

        self.assertEqual(1, self.g.channels[0]["number"])

        self.assertTrue(
            self.g.channels[149]["icon"].endswith(
                "smoothstreams.tv/assets/images/channels/150.png"
            )
        )

    @patch("urllib.request.urlopen")
    def test__detect_xml_feed_type(self, mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 200
        cm.info.return_value = {
            "Expires": "Tue, 07 Jan 2020 00:53:17 GMT",
            "Content-Type": "text/xml",
        }
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.assertEqual("text/xml", self.g._get_content_type())

    @patch("urllib.request.urlopen")
    def test__detect_unknown_feed_type(self, mock_urlopen):
        cm = MagicMock()
        cm.getcode.return_value = 404
        cm.info.return_value = {
            "Expires": "Sat, 25 Aug 2018 22:39:41 GMT",
            "Content-Type": "application/html",
        }
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        with self.assertRaises(InvalidContentType):
            Guide()

    @patch("urllib.request.urlopen")
    def test__gzipped_feed(self, mock_urlopen):
        with open("tests/test_xmltv1.xml.gz", "rb") as f:
            feed = f.read()

        cm = MagicMock()
        cm.read.return_value = feed  # No decode, already bytes
        cm.info.return_value = {
            "Expires": "Tue, 07 Jan 2020 00:53:17 GMT",
            "Content-Type": "application/octet-stream",
        }
        cm.__enter__.return_value = cm
        mock_urlopen.return_value = cm

        self.assertEqual(150, len(self.g.channels))

    @patch("urllib.request.urlopen")
    def test__add_xml_declaration(self, mock_urlopen):
        with open("./tests/test_altepg1.xml", "r") as f:
            json_feed = f.read()

            cm = MagicMock()
            cm.getcode.return_value = 200
            cm.read.return_value = json_feed.encode()
            cm.info.return_value = {
                "Expires": "Sat, 25 Aug 2018 22:39:41 GMT",
                "Content-Type": "text/xml",
            }
            cm.__enter__.return_value = cm
            mock_urlopen.return_value = cm

            g = Guide(Feed.ALTEPG)
            self.assertTrue(g.epg_data.startswith(b"<?xml version"))
