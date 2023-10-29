// Licensed to the .NET Foundation under one or more agreements.
// The .NET Foundation licenses this file to you under the MIT license.

using System;
using System.Collections;
using System.Collections.Generic;
using Jokersoft.AspNetCore.JsonPatch;
using Microsoft.Extensions.Internal;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Newtonsoft.Json.Serialization;

namespace Microsoft.AspNetCore.JsonPatch.Internal;

/// <summary>
/// This API supports infrastructure and is not intended to be used
/// directly from your code. This API may change or be removed in future releases.
/// </summary>
public class ListAdapter : IAdapter
{
    public virtual bool TryAdd(
        object target,
        string segment,
        IContractResolver contractResolver,
        object value,
        out string errorMessage)
    {
        var list = (IList)target;

        if (!TryGetListTypeArgument(list, out var typeArgument, out errorMessage))
        {
            return false;
        }

        if (!TryGetPositionInfo(list, segment, OperationType.Add, out var positionInfo, out errorMessage))
        {
            return false;
        }

        if (!TryConvertValue(value, typeArgument, segment, contractResolver, out var convertedValue, out errorMessage))
        {
            return false;
        }

        if (positionInfo.Type == PositionType.EndOfList)
        {
            list.Add(convertedValue);
        }
        else
        {
            list.Insert(positionInfo.Index, convertedValue);
        }

        errorMessage = null;
        return true;
    }

    public virtual bool TryGet(
        object target,
        string segment,
        IContractResolver contractResolver,
        out object value,
        out string errorMessage)
    {
        var list = (IList)target;

        if (!TryGetListTypeArgument(list, out _, out errorMessage))
        {
            value = null;
            return false;
        }

        if (!TryGetPositionInfo(list, segment, OperationType.Get, out var positionInfo, out errorMessage))
        {
            value = null;
            return false;
        }

        if (positionInfo.Type == PositionType.EndOfList)
        {
            value = list[list.Count - 1];
        }
        else
        {
            value = list[positionInfo.Index];
        }

        errorMessage = null;
        return true;
    }

    public virtual bool TryRemove(
        object target,
        string segment,
        IContractResolver contractResolver,
        out string errorMessage)
    {
        var list = (IList)target;

        if (!TryGetListTypeArgument(list, out _, out errorMessage))
        {
            return false;
        }

        if (!TryGetPositionInfo(list, segment, OperationType.Remove, out var positionInfo, out errorMessage))
        {
            return false;
        }

        if (positionInfo.Type == PositionType.EndOfList)
        {
            list.RemoveAt(list.Count - 1);
        }
        else
        {
            list.RemoveAt(positionInfo.Index);
        }

        errorMessage = null;
        return true;
    }

    public virtual bool TryReplace(
        object target,
        string segment,
        IContractResolver contractResolver,
        object value,
        out string errorMessage)
    {
        var list = (IList)target;

        if (!TryGetListTypeArgument(list, out var typeArgument, out errorMessage))
        {
            return false;
        }

        if (!TryGetPositionInfo(list, segment, OperationType.Replace, out var positionInfo, out errorMessage))
        {
            return false;
        }

        if (!TryConvertValue(value, typeArgument, segment, contractResolver, out var convertedValue, out errorMessage))
        {
            return false;
        }

        if (positionInfo.Type == PositionType.EndOfList)
        {
            list[list.Count - 1] = convertedValue;
        }
        else
        {
            list[positionInfo.Index] = convertedValue;
        }

        errorMessage = null;
        return true;
    }

    public virtual bool TryTest(
        object target,
        string segment,
        IContractResolver contractResolver,
        object value,
        out string errorMessage)
    {
        var list = (IList)target;

        if (!TryGetListTypeArgument(list, out var typeArgument, out errorMessage))
        {
            return false;
        }

        if (!TryGetPositionInfo(list, segment, OperationType.Replace, out var positionInfo, out errorMessage))
        {
            return false;
        }

        if (!TryConvertValue(value, typeArgument, segment, contractResolver, out var convertedValue, out errorMessage))
        {
            return false;
        }

        var currentValue = list[positionInfo.Index];
        if (!JToken.DeepEquals(JsonConvert.SerializeObject(currentValue), JsonConvert.SerializeObject(convertedValue)))
        {
            errorMessage = Resources.FormatValueAtListPositionNotEqualToTestValue(currentValue, value, positionInfo.Index);
            return false;
        }
        else
        {
            errorMessage = null;
            return true;
        }
    }

    public virtual bool TryTraverse(
        object target,
        string segment,
        IContractResolver contractResolver,
        out object value,
        out string errorMessage)
    {
        var list = target as IList;
        if (list == null)
        {
            value = null;
            errorMessage = null;
            return false;
        }

        if (!int.TryParse(segment, out var index))
        {
            value = null;
            errorMessage = Resources.FormatInvalidIndexValue(segment);
            return false;
        }

        if (index < 0 || index >= list.Count)
        {
            value = null;
            errorMessage = Resources.FormatIndexOutOfBounds(segment);
            return false;
        }

        value = list[index];
        errorMessage = null;
        return true;
    }

    protected virtual bool TryConvertValue(
        object originalValue,
        Type listTypeArgument,
        string segment,
        out object convertedValue,
        out string errorMessage)
    {
        return TryConvertValue(
            originalValue,
            listTypeArgument,
            segment,
            null,
            out convertedValue,
            out errorMessage);
    }

    protected virtual bool TryConvertValue(
        object originalValue,
        Type listTypeArgument,
        string segment,
        IContractResolver contractResolver,
        out object convertedValue,
        out string errorMessage)
    {
        var conversionResult = ConversionResultProvider.ConvertTo(originalValue, listTypeArgument, contractResolver);
        if (!conversionResult.CanBeConverted)
        {
            convertedValue = null;
            errorMessage = Resources.FormatInvalidValueForProperty(originalValue);
            return false;
        }

        convertedValue = conversionResult.ConvertedInstance;
        errorMessage = null;
        return true;
    }

    protected virtual bool TryGetListTypeArgument(IList list, out Type listTypeArgument, out string errorMessage)
    {
        // Arrays are not supported as they have fixed size and operations like Add, Insert do not make sense
        var listType = list.GetType();
        if (listType.IsArray)
        {
            errorMessage = Resources.FormatPatchNotSupportedForArrays(listType.FullName);
            listTypeArgument = null;
            return false;
        }
        else
        {
            var genericList = ClosedGenericMatcher.ExtractGenericInterface(listType, typeof(IList<>));
            if (genericList == null)
            {
                errorMessage = Resources.FormatPatchNotSupportedForNonGenericLists(listType.FullName);
                listTypeArgument = null;
                return false;
            }
            else
            {
                listTypeArgument = genericList.GenericTypeArguments[0];
                errorMessage = null;
                return true;
            }
        }
    }

    protected virtual bool TryGetPositionInfo(
        IList list,
        string segment,
        OperationType operationType,
        out PositionInfo positionInfo,
        out string errorMessage)
    {
        if (segment == "-")
        {
            positionInfo = new PositionInfo(PositionType.EndOfList, -1);
            errorMessage = null;
            return true;
        }

        if (int.TryParse(segment, out var position))
        {
            if (position >= 0 && position < list.Count)
            {
                positionInfo = new PositionInfo(PositionType.Index, position);
                errorMessage = null;
                return true;
            }
            // As per JSON Patch spec, for Add operation the index value representing the number of elements is valid,
            // where as for other operations like Remove, Replace, Move and Copy the target index MUST exist.
            else if (position == list.Count && operationType == OperationType.Add)
            {
                positionInfo = new PositionInfo(PositionType.EndOfList, -1);
                errorMessage = null;
                return true;
            }
            else
            {
                positionInfo = new PositionInfo(PositionType.OutOfBounds, position);
                errorMessage = Resources.FormatIndexOutOfBounds(segment);
                return false;
            }
        }
        else
        {
            positionInfo = new PositionInfo(PositionType.Invalid, -1);
            errorMessage = Resources.FormatInvalidIndexValue(segment);
            return false;
        }
    }

    /// <summary>
    /// This API supports infrastructure and is not intended to be used
    /// directly from your code. This API may change or be removed in future releases.
    /// </summary>
    protected readonly struct PositionInfo
    {
        public PositionInfo(PositionType type, int index)
        {
            Type = type;
            Index = index;
        }

        public PositionType Type { get; }
        public int Index { get; }
    }

    /// <summary>
    /// This API supports infrastructure and is not intended to be used
    /// directly from your code. This API may change or be removed in future releases.
    /// </summary>
    protected enum PositionType
    {
        Index, // valid index
        EndOfList, // '-'
        Invalid, // Ex: not an integer
        OutOfBounds
    }

    /// <summary>
    /// This API supports infrastructure and is not intended to be used
    /// directly from your code. This API may change or be removed in future releases.
    /// </summary>
    protected enum OperationType
    {
        Add,
        Remove,
        Get,
        Replace
    }
}
