#!/usr/bin/env python
#
# A library that provides a Python interface to the Telegram Bot API
# Copyright (C) 2015-2025
# Leandro Toledo de Souza <devs@python-telegram-bot.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This module contains the classes that represent Telegram InlineQueryResultVoice."""

import datetime as dtm
from collections.abc import Sequence
from typing import TYPE_CHECKING, Optional, Union

from telegram._inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram._inline.inlinequeryresult import InlineQueryResult
from telegram._messageentity import MessageEntity
from telegram._utils.argumentparsing import parse_sequence_arg, to_timedelta
from telegram._utils.datetime import get_timedelta_value
from telegram._utils.defaultvalue import DEFAULT_NONE
from telegram._utils.types import JSONDict, ODVInput, TimePeriod
from telegram.constants import InlineQueryResultType

if TYPE_CHECKING:
    from telegram import InputMessageContent


class InlineQueryResultVoice(InlineQueryResult):
    """
    Represents a link to a voice recording in an .ogg container encoded with OPUS. By default,
    this voice recording will be sent by the user. Alternatively, you can use
    :attr:`input_message_content` to send a message with the specified content instead of
    the voice message.

    .. seealso:: :wiki:`Working with Files and Media <Working-with-Files-and-Media>`

    Args:
        id (:obj:`str`): Unique identifier for this result,
            :tg-const:`telegram.InlineQueryResult.MIN_ID_LENGTH`-
            :tg-const:`telegram.InlineQueryResult.MAX_ID_LENGTH` Bytes.
        voice_url (:obj:`str`): A valid URL for the voice recording.
        title (:obj:`str`): Recording title.
        caption (:obj:`str`, optional): Caption,
            0-:tg-const:`telegram.constants.MessageLimit.CAPTION_LENGTH` characters after entities
            parsing.
        parse_mode (:obj:`str`, optional): |parse_mode|
        caption_entities (Sequence[:class:`telegram.MessageEntity`], optional): |caption_entities|

            .. versionchanged:: 20.0
                |sequenceclassargs|

        voice_duration (:obj:`int` | :class:`datetime.timedelta`, optional): Recording duration
            in seconds.

            .. versionchanged:: v22.2
                |time-period-input|
        reply_markup (:class:`telegram.InlineKeyboardMarkup`, optional): Inline keyboard attached
            to the message.
        input_message_content (:class:`telegram.InputMessageContent`, optional): Content of the
            message to be sent instead of the voice recording.

    Attributes:
        type (:obj:`str`): :tg-const:`telegram.constants.InlineQueryResultType.VOICE`.
        id (:obj:`str`): Unique identifier for this result,
            :tg-const:`telegram.InlineQueryResult.MIN_ID_LENGTH`-
            :tg-const:`telegram.InlineQueryResult.MAX_ID_LENGTH` Bytes.
        voice_url (:obj:`str`): A valid URL for the voice recording.
        title (:obj:`str`): Recording title.
        caption (:obj:`str`): Optional. Caption,
            0-:tg-const:`telegram.constants.MessageLimit.CAPTION_LENGTH` characters after entities
            parsing.
        parse_mode (:obj:`str`): Optional. |parse_mode|
        caption_entities (tuple[:class:`telegram.MessageEntity`]): Optional. |captionentitiesattr|

            .. versionchanged:: 20.0

                * |tupleclassattrs|
                * |alwaystuple|
        voice_duration (:obj:`int` | :class:`datetime.timedelta`): Optional. Recording duration
            in seconds.

            .. deprecated:: v22.2
                |time-period-int-deprecated|
        reply_markup (:class:`telegram.InlineKeyboardMarkup`): Optional. Inline keyboard attached
            to the message.
        input_message_content (:class:`telegram.InputMessageContent`): Optional. Content of the
            message to be sent instead of the voice recording.

    """

    __slots__ = (
        "_voice_duration",
        "caption",
        "caption_entities",
        "input_message_content",
        "parse_mode",
        "reply_markup",
        "title",
        "voice_url",
    )

    def __init__(
        self,
        id: str,  # pylint: disable=redefined-builtin
        voice_url: str,
        title: str,
        voice_duration: Optional[TimePeriod] = None,
        caption: Optional[str] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,
        input_message_content: Optional["InputMessageContent"] = None,
        parse_mode: ODVInput[str] = DEFAULT_NONE,
        caption_entities: Optional[Sequence[MessageEntity]] = None,
        *,
        api_kwargs: Optional[JSONDict] = None,
    ):
        # Required
        super().__init__(InlineQueryResultType.VOICE, id, api_kwargs=api_kwargs)
        with self._unfrozen():
            self.voice_url: str = voice_url
            self.title: str = title

            # Optional
            self._voice_duration: Optional[dtm.timedelta] = to_timedelta(voice_duration)
            self.caption: Optional[str] = caption
            self.parse_mode: ODVInput[str] = parse_mode
            self.caption_entities: tuple[MessageEntity, ...] = parse_sequence_arg(caption_entities)
            self.reply_markup: Optional[InlineKeyboardMarkup] = reply_markup
            self.input_message_content: Optional[InputMessageContent] = input_message_content

    @property
    def voice_duration(self) -> Optional[Union[int, dtm.timedelta]]:
        return get_timedelta_value(self._voice_duration, attribute="voice_duration")
